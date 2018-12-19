import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

# (a)
# Read the Lahman "pitching.csv" data file into R into a dataframe Pitching
chapter_path = "C:/Users/conno/Documents/GitHub/Baseball/Analyzing Baseball Data With R/Book - First Edition/Chapter 2 - Introduction to R"
os.chdir(chapter_path)
Pitching = pd.read_csv("pitching.csv")

# (b)
# The following function computes the comulative strikeouts, cumulative walks,
# mid career year, and total innings pitched (in terms of outs) for a pitcher
# whose season statistics are stored in the datafrme d

def stats(df):
    ''' Function that returns a dataframe of a players career SO, BB, IPouts, 
    midYear from a dataframe that has individual year data'''
    d = dict()
    d['playerID'] = df['playerID'].unique()
    d['SO'] = sum(df['SO'])
    d['BB'] = sum(df['BB'])
    d['IPouts'] = sum(df['IPouts'])
    d['midYear'] = np.median(df['yearID'])
    return pd.DataFrame.from_dict(d)

# Using the funciton ddply together with the function stats, find the career
# statistics for all pitchers in the pitching dataset. Call this new data
# frame career.pitching
career_pitching = Pitching.groupby('playerID').apply(stats)

# (c)
# Use the merge function to merge the Pitching and career.pitching data frames
Pitching = pd.merge(Pitching, career_pitching, on="playerID")

# (d)
# Use the subset function to construct a new data frame career.10000
# consisting of data for only those pitchers with at least 10,000 career
# IPouts
career_10000 = career_pitching[career_pitching['IPouts'] >= 10000]

# (e)
# For the pitchers with at least 10,000 career IPouts, construct a scatterplot
# of mid career year and ratio of strikeouts to walks. Comment on the general
# pattern in this scatterplot
career_10000['SO_BB_Ratio'] = career_10000['SO'] / career_10000['BB']
plt.scatter(career_10000['midYear'], career_10000['SO_BB_Ratio'])

# The strikeout to walk ratio increases over time as Mid Year increases
