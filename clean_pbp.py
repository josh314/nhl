"""
Clean the raw seasonal play-by-play files (CSV) from WAR-On-Ice. 

1.) Change WAR-On-Ice's eccentric choice of abbreviations for some team names. I use the standard ones used by the NHL

2.) Drop the first column which is just the row number, so kinda redundant 

3.) Just opening and then resaving in pandas will get rid of all of the double quotes cluttering up the file
"""
import sys

if __name__ == '__main__' and len(sys.argv) < 2:
    sys.exit("Usage: clean_pbp <input CSV> <optional output CSV>")

    
import pandas as pd
import numpy as np


def std_team_names(df):
    """
    Changing WAR-On-Ice's eccentric choice of abbreviations for some team names. I change the abbreviations to the standard ones used by the NHL
    """
    # Abbreviations replacment map
    abbrev_map = {
        'L.A':'LAK',
        'N.J':'NJD',
        'S.J':'SJS',
        'T.B':'TBL'
    }
    # Perform replacments
    for old,new in abbrev_map.items():
        df.replace(old,new,inplace=True)

def set_io_files():
    infile = sys.argv[1]
    outfile = "out.csv"
    if len(sys.argv) > 2:
        outfile = sys.argv[2]
    return (infile,outfile)

def main():
    infile, outfile = set_io_files()
    raw = pd.read_csv(infile,header=0)
    # Drop unnamed redundant index column
    raw.drop(raw.columns[0], axis=1, inplace=True)
    # Remove the 'no player' placeholders
#raw.replace(
    #Set the standard team abbreviations
    std_team_names(raw)
    raw.to_csv(outfile,index=False)

if __name__ == '__main__':
    main()

