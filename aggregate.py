"""
Functions to perform aggregation on the cleaned WAR-On-Ice data. 
"""
import pandas as pd
import numpy as np
import nhl.event_filter as evfilter
import nhl.constants as const

############### Team Aggregation #############################

def team_record(events,team,filter_fn=None):#TODO
    if(filter_fn == 'home'):
        filter_fn = evfilter.by_home_team
    elif(filter_fn == 'away'):
        filter_fn = evfilter.by_away_team
    else:
        filter_fn = evfilter.by_team
    ev = filter_fn(events,team)

    
#################################################################


############### Skaters Aggregation #############################

def players_goals(events):
    goals = evfilter.goals(events)
    players_goals = goals.groupby('ev.player.1').size()
    players_goals.index.name = 'player'
    return players_goals

def players_assists(events):
    goals = evfilter.goals(events)
    players_assists = pd.melt(goals[['ev.player.2','ev.player.3']]).dropna().groupby('value').size()
    return players_assists
    
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

def goalie_records(events,goalie_index=None):
    "Aggregate goalie win/loss record over input events. Returns data frame with total wins/losses, and home & away win/losses. A win/loss is recorded only if the goalie is on the ice for the game-winning-goal. A list or index of goalies can be input if already calculated; otherwise computed on the fly from events."
    g = evfilter.game_winning_goals(events)
    wins = {t:  g[g['ev.team']==g[t + 'team']] for t in ['home','away']} 
    records = {
        'home_wins': wins['home'].groupby('home.G').size(),
        'home_losses': wins['away'].groupby('home.G').size(),
        'away_wins': wins['away'].groupby('away.G').size(),
        'away_losses': wins['home'].groupby('away.G').size(),
        }
    index = goalie_index if goalie_index is not None else _goalie_index(events)
    res = pd.DataFrame(index=index, data=records).fillna(0)
    res.insert(0,'losses', res['home_losses'] + res['away_losses'])
    res.insert(0,'wins', res['home_wins'] + res['away_wins'])
    return res
    
def goalies_games_started(events,goalie_index=None):
    "Aggregate goalie starts over input events. A list or index of goalies can be input if already calculated; otherwise computed on the fly from events. Returns data frame with columns: (starts,home_starts,away_starts)."
    index = goalie_index if goalie_index is not None else _goalie_index(events)
    res = pd.DataFrame(index=index)
    games = events.groupby('gcode').head(1)
    res.insert(len(res.columns),'home_starts',games['home.G'].value_counts())
    res.insert(len(res.columns),'away_starts',games['away.G'].value_counts())
    res.fillna(0,inplace=True)
    res.insert(0,'starts',res['home_starts']+res['away_starts'])
    return res
    
def goals_against(events):
    "Aggregate goals against for individual goalies over the input set of events. Returns a series indexed by goalie text_id."
    goals = evfilter.goals(events)
    goalies = pd.Series(data=goals['home.G'],index=goals.index)
    goalies[goals['ev.team']==goals['hometeam']] = goals['away.G']
    return goalies.dropna().value_counts().sort_index()

def saves(events):
    "Aggregate saves for individual goalies over the input set of events. Returns a series indexed by goalie text_id."
    saved_shots = evfilter.saves(events)
    goalie = pd.Series(data=saved_shots['home.G'],index=saved_shots.index)
    goalie[saved_shots['ev.team']==saved_shots['hometeam']] = saved_shots['away.G']
    return goalie.dropna().value_counts().sort_index()

def goalies_stats(events):#WIP
    "Individual goalie data aggregated over the input events"
    stats = pd.DataFrame(index=_goalie_index(events))
    stats.insert(len(stats.columns),'goals_against',goals_against(events))
    stats.insert(len(stats.columns),'saves', saves(events))
    stats = stats.join(goalie_records(events,stats.index))
    stats.fillna(0,inplace=True)
    stats.insert(len(stats.columns), 'shots_against', (stats['saves']+stats['goals_against']))
    stats.insert(len(stats.columns), 'save%', stats['saves']/(stats['saves']+stats['goals_against']))
    return stats

def goalie_stats(events,player):#WIP
    stats = None
    return stats
