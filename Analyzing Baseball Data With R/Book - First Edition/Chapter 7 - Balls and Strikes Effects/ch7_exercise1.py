import pandas as pd
# Run Values of Hits

# In Section 5.8, we found the average run vaalue of a home run and a single

# (a)
# Use similar R code as described in Section 5.8 for the 2011 season data to
# find the mean run values for a double and for a triple

# read in 2011 play by play data
data2011 = pd.read_csv('all2011.csv', header=None)
fields = pd.read_csv('fields.csv')
data2011.columns = fields.loc[:, 'Header']

# We want to calculate the runs scored for the remaining of the inning

# First calculate the runs at a given time
data2011['RUNS'] = data2011.AWAY_SCORE_CT + data2011.HOME_SCORE_CT

# Create a unique ID for each half inning
data2011['HALF_INNING'] = data2011.GAME_ID + data2011.INN_CT.map(str) + \
                            data2011.BAT_HOME_ID.map(str)

# Now we will calculate how many runs were scored at the end of the inning

# Calculate the number of runs scored during each play
data2011['RUNS_SCORED'] = (data2011.BAT_DEST_ID > 3).astype(int) + \
                            (data2011.RUN1_DEST_ID > 3).astype(int) + \
                            (data2011.RUN2_DEST_ID > 3).astype(int) + \
                            (data2011.RUN3_DEST_ID > 3).astype(int)

# Get the Number of runs scored in a specific inning
RUNS_SCORED_INNING = data2011.groupby(['HALF_INNING']).sum().loc[:, 
                                     'RUNS_SCORED']



# Find the total game runs at the beginning of the inning with '[' function 
RUNS_SCORED_START = data2011.loc[:, ['HALF_INNING', 'RUNS']].groupby(
        ['HALF_INNING']).min().loc[:, 'RUNS']

# Get the maximum number of runs in the half inning
MAX = pd.DataFrame(RUNS_SCORED_INNING + RUNS_SCORED_START)
MAX.columns = ['MAX_RUNS']
MAX['half'] = MAX.index

# Merge together the max_runs into the data2011 dataframe
data2011 = data2011.merge(MAX, left_on='HALF_INNING', right_on='half')

# Calculate the runs for the remainder of the inning. Typo in Book
data2011['RUNS_ROI'] = data2011.MAX_RUNS - data2011.RUNS

# Create Binary Variable to determine if runner is on a base before play
RUNNER1 = data2011['BASE1_RUN_ID'].notna().astype(int)
RUNNER2 = data2011['BASE2_RUN_ID'].notna().astype(int)
RUNNER3 = data2011['BASE3_RUN_ID'].notna().astype(int)

# Create the current state 
data2011['STATE'] = RUNNER1.map(str) + RUNNER2.map(str) + RUNNER3.map(str) + \
                    ' ' + data2011.OUTS_CT.map(str)

# Create Binary Variable to determine if a runner is on a base after play
NRUNNER1 = ((data2011.RUN1_DEST_ID == 1) | \
            (data2011.BAT_DEST_ID == 1)).astype(int)

NRUNNER2 = ((data2011.BAT_DEST_ID == 2) | \
            (data2011.RUN1_DEST_ID == 2) | \
            (data2011.RUN2_DEST_ID == 2)).astype(int)

NRUNNER3 = ((data2011.BAT_DEST_ID == 3) | \
            (data2011.RUN1_DEST_ID == 3) | \
            (data2011.RUN2_DEST_ID == 3) | \
            (data2011.RUN3_DEST_ID == 3)).astype(int)

# Get number of outs at the end of play
NOUTS = data2011.OUTS_CT + data2011.EVENT_OUTS_CT

# Get the new state at the end of the play
data2011['NEW_STATE'] = NRUNNER1.map(str) + NRUNNER2.map(str) + \
                        NRUNNER3.map(str) + ' ' + NOUTS.map(str)

# Reduce dataframe to when states change or runs score
data2011 = data2011[(data2011.STATE != data2011.NEW_STATE) | 
            (data2011.RUNS_SCORED > 0)]

# Get the number of outs per inning and merge into the dataframe
OUTS = pd.DataFrame(data2011.loc[:, ['HALF_INNING', 'EVENT_OUTS_CT']].groupby(
        ['HALF_INNING']).sum().loc[:, 'EVENT_OUTS_CT'])
OUTS.columns = ['INNING_OUTS']
OUTS['half'] = OUTS.index
data2011 = data2011.merge(OUTS, left_on='HALF_INNING', right_on='half')

# filter out half innings that are walk-offs because they are not complete
# innings
data2011c = data2011[data2011.INNING_OUTS == 3]

# Calculate the expected number of runs for each element of the matrix
RUNS = pd.DataFrame(data2011c.loc[:, ['STATE', 'RUNS_ROI']].groupby(
        ['STATE']).mean().loc[:, 'RUNS_ROI'])

# Add Three Out States to Create Potential States data frame
s3 = ['000 3', '001 3', '010 3', '011 3', '100 3', '101 3', '110 3', '111 3']
zeros_data = {'RUNS_ROI':[0,0,0,0,0,0,0,0]}
RUNS_POTENTIAL = RUNS.append(pd.DataFrame(data=zeros_data, index=s3))

# Calculate Runs Value of State Before Play
data2011['RUNS_STATE'] = RUNS_POTENTIAL.loc[data2011.
                            STATE,].reset_index().loc[:,'RUNS_ROI']

# Calculate Runs Value of State After Play
data2011['RUNS_NEW_STATE'] = RUNS_POTENTIAL.loc[data2011.
                                NEW_STATE,].reset_index().loc[:,'RUNS_ROI']

# Calculate Runs Value of each play
data2011['RUNS_VALUE'] = data2011.RUNS_NEW_STATE - data2011.RUNS_STATE + \
                            data2011.RUNS_SCORED


# Calculate the value of each count
z = [0,0,0,0,0,0,0,0,0,0,0,0]
counts = ["0-0", "1-0", "2-0", "3-0", "0-1", "1-1", "2-1", "3-1", "0-2", "1-2",
          "2-2", "3-2"]
ct_val = pd.DataFrame({"Value": z})
ct_val.index = counts

d00 = data2011[(data2011.BALLS_CT==0) & (data2011.STRIKES_CT==0)]
d10 = data2011[(data2011.BALLS_CT==1) & (data2011.STRIKES_CT==0)]
d20 = data2011[(data2011.BALLS_CT==2) & (data2011.STRIKES_CT==0)]
d30 = data2011[(data2011.BALLS_CT==3) & (data2011.STRIKES_CT==0)]
d01 = data2011[(data2011.BALLS_CT==0) & (data2011.STRIKES_CT==1)]
d11 = data2011[(data2011.BALLS_CT==1) & (data2011.STRIKES_CT==1)]
d21 = data2011[(data2011.BALLS_CT==2) & (data2011.STRIKES_CT==1)]
d31 = data2011[(data2011.BALLS_CT==3) & (data2011.STRIKES_CT==1)]
d02 = data2011[(data2011.BALLS_CT==0) & (data2011.STRIKES_CT==2)]
d12 = data2011[(data2011.BALLS_CT==1) & (data2011.STRIKES_CT==2)]
d22 = data2011[(data2011.BALLS_CT==2) & (data2011.STRIKES_CT==2)]
d32 = data2011[(data2011.BALLS_CT==3) & (data2011.STRIKES_CT==2)]

# Calculate value for each count
ct_val.loc["0-0", "Value"] = d00.RUNS_VALUE.mean()
ct_val.loc["1-0", "Value"] = d10.RUNS_VALUE.mean()
ct_val.loc["2-0", "Value"] = d20.RUNS_VALUE.mean()
ct_val.loc["3-0", "Value"] = d30.RUNS_VALUE.mean()
ct_val.loc["0-1", "Value"] = d01.RUNS_VALUE.mean()
ct_val.loc["1-1", "Value"] = d11.RUNS_VALUE.mean()
ct_val.loc["2-1", "Value"] = d21.RUNS_VALUE.mean()
ct_val.loc["3-1", "Value"] = d31.RUNS_VALUE.mean()
ct_val.loc["0-2", "Value"] = d02.RUNS_VALUE.mean()
ct_val.loc["1-2", "Value"] = d12.RUNS_VALUE.mean()
ct_val.loc["2-2", "Value"] = d22.RUNS_VALUE.mean()
ct_val.loc["3-2", "Value"] = d32.RUNS_VALUE.mean()

# Calculate the value of balls and strikes in each count

ct_val = pd.DataFrame({"Value": z})
ct_val.index = ["0-0", "1-0", "2-0", "3-0", "0-1", "1-1", "2-1", "3-1", "0-2",
                "1-2", "2-2", "3-2"]

bs_val = pd.DataFrame({"Strike": z, "Ball": z})
bs_val.index = counts

# Mean value of strikeout
d_strikeout = data2011[data2011.EVENT_CD == 3]
strikeout_val = d_strikeout.RUNS_VALUE.mean()

# Mean value of walk
d_walk = data2011[data2011.EVENT_CD == 14]
walk_val = d_walk.RUNS_VALUE.mean()

# Calculate Values of different pitches for Strikes
bs_val.loc["0-0", "Strike"] = round(ct_val.loc["0-1", "Value"] - 
      ct_val.loc["0-0", "Value"], 2)
bs_val.loc["1-0", "Strike"] = round(ct_val.loc["1-1", "Value"] - 
      ct_val.loc["1-0", "Value"], 2)
bs_val.loc["2-0", "Strike"] = round(ct_val.loc["2-1", "Value"] - 
      ct_val.loc["2-0", "Value"], 2)
bs_val.loc["3-0", "Strike"] = round(ct_val.loc["3-1", "Value"] - 
      ct_val.loc["3-0", "Value"], 2)

bs_val.loc["0-1", "Strike"] = round(ct_val.loc["0-2", "Value"] - 
      ct_val.loc["0-1", "Value"], 2)
bs_val.loc["1-1", "Strike"] = round(ct_val.loc["1-2", "Value"] - 
      ct_val.loc["1-1", "Value"], 2)
bs_val.loc["2-1", "Strike"] = round(ct_val.loc["2-2", "Value"] - 
      ct_val.loc["2-1", "Value"], 2)
bs_val.loc["3-1", "Strike"] = round(ct_val.loc["3-2", "Value"] - 
      ct_val.loc["3-1", "Value"], 2)

bs_val.loc["0-2", "Strike"] = round(strikeout_val - 
          ct_val.loc["0-2", "Value"], 2)
bs_val.loc["1-2", "Strike"] = round(strikeout_val - 
          ct_val.loc["1-2", "Value"], 2)
bs_val.loc["2-2", "Strike"] = round(strikeout_val - 
          ct_val.loc["2-2", "Value"], 2)
bs_val.loc["3-2", "Strike"] = round(strikeout_val - 
          ct_val.loc["3-2", "Value"], 2)

# Calculate Values of different pitches for Balls
bs_val.loc["0-0", "Ball"] = round(ct_val.loc["1-0", "Value"] - 
      ct_val.loc["0-0", "Value"], 2)
bs_val.loc["1-0", "Ball"] = round(ct_val.loc["2-0", "Value"] - 
      ct_val.loc["1-0", "Value"], 2)
bs_val.loc["2-0", "Ball"] = round(ct_val.loc["3-0", "Value"] - 
      ct_val.loc["2-0", "Value"], 2)
bs_val.loc["3-0", "Ball"] = round(walk_val - ct_val["3-0", "Value"], 2)

bs_val.loc["0-1", "Ball"] = round(ct_val.loc["1-1", "Value"] - 
      ct_val.loc["0-1", "Value"], 2)
bs_val.loc["1-1", "Ball"] = round(ct_val.loc["2-1", "Value"] - 
      ct_val.loc["1-1", "Value"], 2)
bs_val.loc["2-1", "Ball"] = round(ct_val.loc["3-1", "Value"] - 
      ct_val.loc["2-1", "Value"], 2)
bs_val.loc["3-1", "Ball"] = round(walk_val - ct_val["3-1", "Value"], 2)

bs_val.loc["0-2", "Ball"] = round(ct_val.loc["1-2", "Value"] - 
      ct_val.loc["0-2", "Value"], 2)
bs_val.loc["1-2", "Ball"] = round(ct_val.loc["2-2", "Value"] - 
      ct_val.loc["1-2", "Value"], 2)
bs_val.loc["2-2", "Ball"] = round(ct_val.loc["3-2", "Value"] - 
      ct_val.loc["2-2", "Value"], 2)
bs_val.loc["3-2", "Ball"] = round(walk_val - ct_val.loc["3-2", "Value"], 2)

# (b)
# Compare your values to the ones proposed by John Walsh in the article 
# www.hardballtimes.com/main/article/searching-for-the-games-best-pitch

# The values are similar to those in the fangraphs article. They possibly
# have a smaller magnitude


