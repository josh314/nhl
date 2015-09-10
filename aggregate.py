"""
Perform aggragation on the cleaned WAR-On-Ice play-by-play files.
"""
import sys

if __name__ == '__main__' and len(sys.argv) < 2:
    sys.exit("Usage: aggregate <input CSV> <optional output CSV>")

    
import pandas as pd
import numpy as np


def set_io_files():
    infile = sys.argv[1]
    outfile = "out.csv"
    if len(sys.argv) > 2:
        outfile = sys.argv[2]
    return (infile,outfile)

def main():
    infile, outfile = set_io_files()
    dat = pd.read_csv(infile,header=0)

    out = pd.DataFrame()
    out.to_csv(outfile,index=False)

if __name__ == '__main__':
    main()
