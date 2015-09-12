"""
Perform aggragation on the cleaned WAR-On-Ice data.
"""
import sys

if __name__ == '__main__' and len(sys.argv) < 2:
    sys.exit("Usage: aggregate <input CSV> <optional output CSV>")

    
import pandas as pd
import numpy as np

def skaters_total_scoring(dat):
    pass

def init_goalie_table(dat):
    # dropna() removes nan from empty net situations
    def uniq_col(x): return set(dat[x].dropna().unique()) 
    goalies = sorted( list( uniq_col('away.G').union( uniq_col('home.G') ) ) )
    return pd.DataFrame(index=goalies)

def aggregate_goals_against(dat):
    goals = dat[dat['etype']=='GOAL']
    goals_against_goalie = pd.Series(data=goals['home.G'],index=goals.index)
    goals_against_goalie[goals['ev.team']==goals['hometeam']] = goals['away.G']
    return goals_against_goalie.dropna().value_counts().sort_index()
    
def goalies_all_stats(dat):
    "Individual goalie data aggregated over all games and game situations"
    goalies = init_goalie_table(dat)
    goalies.insert(0,'GA',aggregate_goals_against(dat))
    return goalies
    
    
def _set_io_files():
    infile = sys.argv[1]
    outfile = "out.csv"
    if len(sys.argv) > 2:
        outfile = sys.argv[2]
    return (infile,outfile)

def _main():
    infile, outfile = _set_io_files()
    dat = pd.read_csv(infile,header=0)

    #out = full_aggregation(dat)
    out.to_csv(outfile,index=False)

if __name__ == '__main__':
    #_main()
    pass
