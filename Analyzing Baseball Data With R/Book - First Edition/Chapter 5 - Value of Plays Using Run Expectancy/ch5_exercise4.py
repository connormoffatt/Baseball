# In Section 5.3, the construction of the run expectancy matrix from 2011
# season data was illustrated. Suppose instead that one was interested in 
# computing the proportion of times when at least one run was scored for each
# of the 24 possible bases/outs situations. Use R to construct this probability
# of scoring matrix
import pandas as pd


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

# Calculate whether a run scored in the inning
data2011['IF_SCORED'] = (data2011.MAX_RUNS - data2011.RUNS > 0).astype(int)

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

# Calculate the probability that a run was scored in the inning for each
# situation
RUNS = pd.DataFrame(data2011c.loc[:, ['STATE', 'IF_SCORED']].groupby(
        ['STATE']).mean().loc[:, 'IF_SCORED'])

# In Section 5.3, the construction of the run expectancy matrix from 2011
# season data was illustrated. Suppose instead that one was interested in 
# computing the proportion of times when at least one run was scored for each
# of the 24 possible bases/outs situations. Use R to construct this probability
# of scoring matrix
                            
