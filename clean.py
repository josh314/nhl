"""
Module for cleaning the raw seasonal play-by-play data from WAR-On-Ice. If run as a script, ingests a cCSV and outputs a CSV.
"""
import sys

if __name__ == '__main__' and len(sys.argv) < 2:
    sys.exit("Usage: clean_pbp <input CSV> <optional output CSV>")

    
import pandas as pd
import numpy as np


def std_team_names(df):
    "Changes WAR-On-Ice's eccentric choice of abbreviations for some team names. I change the abbreviations to the standard ones used by the NHL"
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

def remove_noplayer_placeholders(df):
    "Replaces the 'xxxxxxxNA' placeholders with empty strings."
    df.replace('xxxxxxxNA','',inplace=True)

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
    remove_noplayer_placeholders(raw)
    #Set the standard team abbreviations
    std_team_names(raw)
    raw.to_csv(outfile,index=False)

if __name__ == '__main__':
    main()

