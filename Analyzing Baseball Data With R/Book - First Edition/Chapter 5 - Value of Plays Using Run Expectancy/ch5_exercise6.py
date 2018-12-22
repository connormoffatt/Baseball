# Hitting Evaluation of Player Run Values

# Choose several players who were good hitters in the 2011 season. For each
# player, find the run values and the runners on base for all plate appearances
# As in Figure 5.1 construct a graph of the run values against the runners on
# base. Was this particular batter successful when there were runners in 
# scoring position

# Adrian Gonzalez
# Michael Young
# Jose  Reyes

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

# Choose several players who were good hitters in the 2011 season. For each
# player, find the run values and the runners on base for all plate appearances
# As in Figure 5.1 construct a graph of the run values against the runners on
# base. Was this particular batter successful when there were runners in 
# scoring position

# Adrian Gonzalez
# Michael Young
# Jose  Reyes
                            

# Read in 2011 roster data
roster = pd.read_csv("roster2011.csv")

# Get id's for the three players
gonz_id = roster[(roster['First.Name'] == 'Adrian') & \
                 (roster['Last.Name'] == 'Gonzalez')]
gonz_id = gonz_id.loc[gonz_id.index[0], 'Player.ID']

young_id = roster[(roster['First.Name'] == 'Michael') & \
                 (roster['Last.Name'] == 'Young')]
young_id = young_id.loc[young_id.index[0], 'Player.ID']

reyes_id = roster[(roster['First.Name'] == 'Jose') & \
                 (roster['Last.Name'] == 'Reyes')]
reyes_id = reyes_id.loc[reyes_id.index[0], 'Player.ID']

# Get dataframes of only the players
gonz = data2011[(data2011.BAT_ID == gonz_id) & (data2011.BAT_EVENT_FL == 'T')]
young = data2011[(data2011.BAT_ID == young_id) & (data2011.BAT_EVENT_FL == 'T')]
reyes = data2011[(data2011.BAT_ID == reyes_id) & (data2011.BAT_EVENT_FL == 'T')]

# Get the number of situations with runners and plot against values
gonz['RUNNERS'] = gonz.loc[:, 'STATE'].str[:3]
young['RUNNERS'] = young.loc[:, 'STATE'].str[:3]
reyes['RUNNERS'] = reyes.loc[:, 'STATE'].str[:3]

fig_gonz, ax_gonz = plt.subplots()
strip_gonz = sns.stripplot(x=gonz['RUNS_VALUE'], y=gonz['RUNNERS'], jitter=1,
                           orient='h')
ax_gonz.set(title='Adrian Gonzalez Run Values')

fig_young, ax_young = plt.subplots()
strip_young = sns.stripplot(x=young['RUNS_VALUE'], y=young['RUNNERS'], jitter=1,
                           orient='h')
ax_young.set(title='Michael young Run Values')

fig_reyes, ax_reyes = plt.subplots()
strip_reyes = sns.stripplot(x=reyes['RUNS_VALUE'], y=reyes['RUNNERS'], jitter=1,
                           orient='h')
ax_reyes.set(title='Jose Reyes Run Values')

# Adrain Gonzalez was more unsuccessful than successful with runners in 
# scoring position

# Michael Young was more unsuccessful than successful with runners in 
# scoring position

# Jose Reyes was more unsuccessful than successful with runners in 
# scoring position


