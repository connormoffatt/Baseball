import pandas as pd
import matplotlib.pyplot as plt

# In Section 3.9, we used the Retrosheet play-by-play data to explore the home
# run race between mark McGwire and Sammy Sosa in the 1998 season. Another way
# to compare the patterns of home run hitting of the two players i sto 
# compute the spacings, the number of plate appearnces between homme runs

# (a)
# Following the work of Section 3.9, create two data frames mac.data and
# sosa.data containing the batting  data for the two players

# read in 1998 play by play data and headers
data_1998 = pd.read_csv('./all1998.csv')
fields = pd.read_csv('./fields.csv')

# Change column names in R
data_1998.columns = fields.loc[:,"Header"]

# Find the id for Sosa and McGwire. id's for retrosheet are in retrosheetIDs
retro_ids = pd.read_csv('./retrosheetIDs.csv')
sosa_id = retro_ids[retro_ids[' FIRST'] == 'Sammy']
sosa_id = sosa_id[sosa_id['LAST'] == 'Sosa']
sosa_id=  sosa_id[' ID'].values[0]

mac_id = retro_ids[retro_ids[' FIRST'] == 'Mark']
mac_id = mac_id[mac_id['LAST'] == 'McGwire']
mac_id = mac_id[' ID'].values[0]

# Create player dataframes for every event when they were the batter
sosa_data = data_1998[data_1998['BAT_ID'] == sosa_id]
mac_data = data_1998[data_1998['BAT_ID'] == mac_id]

# (b)
# Use the following R commands to restrict the two data frames to the plays
# where a batting event occurred
mac_data = mac_data[mac_data['BAT_EVENT_FL'] == 'T']
sosa_data = sosa_data[sosa_data['BAT_EVENT_FL'] == 'T']

# (c)
# For each data frame, create a new variable PA that numbers the plate
# appearances 1, 2, ... (The function nrow gives the number of rows of a
# data frame)
mac_data = mac_data.reset_index()
mac_data['PA'] = mac_data.index + 1
sosa_data = sosa_data.reset_index()
sosa_data['PA'] = sosa_data.index + 1

# (d)
# The following commands will return the numbers of the plate appearances when
# the players hit home runs
mac_HR_PA = mac_data[mac_data['EVENT_CD'] == 23]
sosa_HR_PA = sosa_data[sosa_data['EVENT_CD'] == 23]


# (e)
# Using the R function diff, the following commands compute the spacings 
# between the occurrences of home runs
mac_spacings = []
sosa_spacings = []
    
mac_HR_PA = mac_HR_PA.reset_index()
sosa_HR_PA = sosa_HR_PA.reset_index()
    
for i in range(len(mac_HR_PA) - 1):
    PA_diff = mac_HR_PA.at[i + 1, 'PA'] - mac_HR_PA.at[i, 'PA']
    mac_spacings.append(PA_diff)
    
for i in range(len(sosa_HR_PA) - 1):
    PA_diff = sosa_HR_PA.at[i + 1, 'PA'] - sosa_HR_PA.at[i, 'PA']
    sosa_spacings.append(PA_diff)

# (f)
# By use of the summary and hist functions on the vectors mac.spacings and
# sosa.spacings, compare the home run spacings of the two players
fig, ax = plt.subplots()
ax.hist(mac_spacings)
ax.set(title='Mark McGwire Home Run Spacing', xlabel='PA Between HR',
       ylabel='Frequency')
fig, ax = plt.subplots()
ax.hist(sosa_spacings)
ax.set(title='Sammy Sosa Home Run Spacing', xlabel='PA Between HR',
       ylabel='Frequency')

# We see that Mark McGwire Hit had less spacing than Sammy Sosa. Also, we notice
# however, that Sosa's has a large spacing near 50 plate appearances
