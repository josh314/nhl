"""
Perform aggragation on the cleaned WAR-On-Ice data.
"""
import sys

if __name__ == '__main__' and len(sys.argv) < 2:
    sys.exit("Usage: aggregate <input CSV> <optional output CSV>")

    
import pandas as pd
import numpy as np

def skaters_total_scoring(events):
    pass

def _init_goalie_table(events):
    # dropna() removes nan from empty net situations
    def uniq_col(x): return set(events[x].dropna().unique()) 
    goalies = sorted( list( uniq_col('away.G').union(uniq_col('home.G')) ) )
    return pd.DataFrame(index=goalies)

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

def goalies_aggregation_stats(events):
    "Individual goalie data aggregated over the input events"
    goalies = _init_goalie_table(events)
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

def _main():
    infile, outfile = _set_io_files()
    events = pd.read_csv(infile,header=0)

    #out = full_aggregation(events)
    out.to_csv(outfile,index=False)

if __name__ == '__main__':
    #_main()
    pass
