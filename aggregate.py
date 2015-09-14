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

def skaters_total_scoring(events):#TODO
    pass

def _goalie_index(events):
    # dropna() removes nan from empty net situations
    def uniq_col(x): return set(events[x].dropna().unique()) 
    goalies = sorted( list( uniq_col('away.G').union(uniq_col('home.G')) ) )
    return pd.Index(goalies)

def goalies_games_played(events):#TODO
    games = events['gcode'].unique()
    for game in games:
        pass

def game_winning_goals(events):
    "Returns the subset of the input events which represent game winning goals. Shootout goals should be filtered out of input."
    goals = events[events['etype']=='GOAL']
    games = goals.groupby('gcode')
    return games.apply(_find_gwg)
    
def _find_gwg(game_goals):#Returns empty df if a tie
    def _max_score(team):#team = 'home' or 'away'
        return game_goals[team+'.score'].max()
    winner, loser = 'home', 'away'
    if _max_score('away') > _max_score('home'):
        winner, loser = 'away', 'home'
    gwg = game_goals[game_goals[winner+'.score'] > _max_score(loser)].head(1)
    return gwg

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
