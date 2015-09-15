"""
Perform aggregation on the cleaned WAR-On-Ice data. 
"""
import sys

if __name__ == '__main__' and len(sys.argv) < 2:
    sys.exit("Usage: aggregate <input CSV> <optional output CSV>")

import pandas as pd
import numpy as np

### Magic numbers #########
_playoff_gcode_start = 30000
###########################

#################### Event Filters ##############################

def filter_by_hometeam(events,team):
    "Returns events from homes games for `team` (use the standard 3-letter abbreviation for team names.)"
    return events[events['hometeam']==team]

def filter_by_awayteam(events,team):
    "Returns events from away games for `team` (use the standard 3-letter abbreviation for team names.)"
    return events[events['awayteam']==team]

def filter_by_team(events,team):
    "Returns events from all games for `team` (use the standard 3-letter abbreviation for team names.)"
    home = filter_by_hometeam(events,team)
    away = filter_by_awayteam(events,team)
    return home.append(away).sort(axis=0)

def filter_by_event_team(events,team):
    "Returns events where event team is `team` (use the standard 3-letter abbreviation for team names.)"
    return events[events['ev.team']==team]

def remove_shootouts(events):
    "Removes all shootout events."
    # Shootouts are period 5 of regular season games. 
    return events[(events['period']!=5)
                    | (events['gcode'] > _playoff_gcode_start)]

def shootouts(events):
    "Returns only shootout events."
    # Shootouts are period 5 of regular season games. 
    return events[(events['period'] == 5)
                    & (events['gcode'] <= _playoff_gcode_start)]

def even_strength(events):
    #TODO
    return events

def power_play(events):
    #TODO
    return events

def penalty_kill(events):
    #TODO
    return events

def regular_season(events):
    return events[events['gcode'] <= _playoff_gcode_start]

def playoffs(events):
    return events[events['gcode'] > _playoff_gcode_start]

def game_winning_goals(events):
    "Returns subset of the input events which represent game winning goals."
    goals = remove_shootouts(events[events['etype']=='GOAL'])
    games = goals.groupby('gcode')
    def _find_gwg(game_goals):#Returns empty df if a tie
        def _max_score(team):#team = 'home' or 'away'
            score = game_goals[team+'.score'].max()
            if(game_goals.tail(1)['ev.team'].values[0]==game_goals[team+'team'].values[0]):
                score += 1 #score entries don't include the goal just scored
            return score
        winner, loser = 'home', 'away'
        if _max_score('away') > _max_score('home'):
            winner, loser = 'away', 'home'
        winner_goals = game_goals[game_goals['ev.team'] == game_goals[winner+'team']]
        return winner_goals[winner_goals[winner+'.score'] + 1 > _max_score(loser)].head(1)
    gwg = games.apply(_find_gwg)
    gwg.index=gwg.index.levels[1]#removes the redundant gcode indexing layer
    return gwg

#################################################################


############### Skaters Aggregation #############################

def skaters_total_scoring(events):#TODO
    pass
#################################################################

############### Goalies Aggregation #############################

def _goalie_index(events):
    # dropna() removes nan from empty net situations
    def uniq_col(x): return set(events[x].dropna().unique()) 
    goalies = sorted( list( uniq_col('away.G').union(uniq_col('home.G')) ) )
    return pd.Index(goalies)


def goalies_games_played(events):#TODO
    games = events['gcode'].unique()
    for game in games:
        pass

def goalie_record(events,goalie_index=None):
    "Aggregate goalie win/loss record over input events. Returns data frame with total wins/losses, and home & away win/losses. A win/loss is recorded only if the goalie is on the ice for the game-winning-goal. A list or index of goalies can be input if already calculated; otherwise computed on the fly from events."
    g = game_winning_goals(events)
    wins = {t:  g[g['ev.team']==g[t + 'team']] for t in ['home','away']} 
    goalie_home_wins = wins['home'].groupby('home.G').size()
    goalie_away_losses = wins['home'].groupby('away.G').size()
    goalie_away_wins = wins['away'].groupby('away.G').size()
    goalie_home_losses = wins['away'].groupby('home.G').size()
    records = {
        'home_wins': wins['home'].groupby('home.G').size(),
        'home_losses': wins['away'].groupby('home.G').size(),
        'away_wins': wins['away'].groupby('away.G').size(),
        'away_losses': wins['away'].groupby('home.G').size(),
        }
    index = goalie_index if goalie_index else _goalie_index(events)
    res = pd.DataFrame(index=index, data=records).fillna(0)
    res.insert(0,'losses', res['home_losses'] +res['away_losses'])
    res.insert(0,'wins', res['home_wins'] +res['away_wins'])
    return res
    
def goalies_games_started(events,goalie_index=None):
    "Aggregate goalie starts over input events. A list or index of goalies can be input if already calculated; otherwise computed on the fly from events. Returns data frame with columns: (starts,home_starts,away_starts)."
    index = goalie_index if goalie_index else _goalie_index(events)
    res = pd.DataFrame(index=index)
    games = events.groupby('gcode').head(1)
    res.insert(len(res.columns),'home_starts',games['home.G'].value_counts())
    res.insert(len(res.columns),'away_starts',games['away.G'].value_counts())
    res.fillna(0,inplace=True)
    res.insert(0,'starts',res['home_starts']+res['away_starts'])
    return res
    
def goals_against(events):
    "Aggregate goals against for individual goalies over the input set of events. Returns a series indexed by goalie text_id."
    goals = events[events['etype']=='GOAL']
    goalies = pd.Series(data=goals['home.G'],index=goals.index)
    goalies[goals['ev.team']==goals['hometeam']] = goals['away.G']
    return goalies.dropna().value_counts().sort_index()

def saves(events):
    "Aggregate saves for individual goalies over the input set of events. Returns a series indexed by goalie text_id."
    saved_shots = events[events['etype']=='SHOT']
    goalie = pd.Series(data=saved_shots['home.G'],index=saved_shots.index)
    goalie[saved_shots['ev.team']==saved_shots['hometeam']] = saved_shots['away.G']
    return goalie.dropna().value_counts().sort_index()

def goalies_aggregation_stats(events):#WIP
    "Individual goalie data aggregated over the input events"
    goalies = pd.DataFrame(index=_goalie_index(events))
    goalies.insert(len(goalies.columns),'goals_against',goals_against(events))
    goalies.insert(len(goalies.columns),'saves', saves(events))
    goalies.fillna(0,inplace=True)
    return goalies

##########################################################

######################### Main ###########################
def _set_io_files():
    infile = sys.argv[1]
    outfile = "out.csv"
    if len(sys.argv) > 2:
        outfile = sys.argv[2]
    return (infile,outfile)

def _main():#WIP
    infile, outfile = _set_io_files()
    events = pd.read_csv(infile,header=0)
    #goalies = goalie_stats()
    #forwards = forward_stats()
    #dmen = dmen_stats()
    #out = full_aggregation(events)
    out.to_csv(outfile,index=False)

if __name__ == '__main__':#WIP
    #_main()
    pass
