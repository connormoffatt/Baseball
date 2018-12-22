# Comparing Two Players with Similar OBPs

# Rickie Weeks (batter id "weekr001") and Michael Bourne (batter id "bourm001")
# both were leadoff hitters during the 2011 season. They had similar 
# on-base-percentages - .350 for Weeks and .349 for Bourne. By exploring
# the run values of these two players, investigate which player was really more
# valuable to his team. Can you explain the difference in run values in 
# terms of traditional batting statistics such as AVG, SLG, or OBP

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

# Rickie Weeks (batter id "weekr001") and Michael Bourne (batter id "bourm001")
# both were leadoff hitters during the 2011 season. They had similar 
# on-base-percentages - .350 for Weeks and .349 for Bourne. By exploring
# the run values of these two players, investigate which player was really more
# valuable to his team. Can you explain the difference in run values in 
# terms of traditional batting statistics such as AVG, SLG, or OBP
                            
# Get id's
weeks_id = "weekr001"
bourne_id = "bourm001"

# Get dataframe of weeks and bourne
weeks = data2011[(data2011.BAT_ID == weeks_id) & \
                 (data2011.BAT_EVENT_FL == 'T')]
bourne = data2011[(data2011.BAT_ID == bourne_id) & \
                  (data2011.BAT_EVENT_FL == 'T')]

# Print run values of each
print(weeks.RUNS_VALUE.sum())
print(bourne.RUNS_VALUE.sum())

# Ricky Weeks is more valuable of a hitter

# For simplicity, we look up the values

# Weeks
  # AVG: .269
  # OBP: .350
  # SLG: .468

# Bourne
  # AVG: .294
  # OBP: .349
  # SLG: .386

# The difference can be attributed to sluggling. Since Weeks hits for more
# power, he generates more runss
            