import pandas as pd

# load in roster data
roster = pd.read_csv('roster2018.csv')

# List of lists of names [['first 1', 'last 1'], ['first 2', 'second 2'],...]
names = [['Albert', 'Pujols'], ['Mike', 'Trout'], ['David', 'Fletcher']]

# LIST TO LIST

id_list = []
for n in names:
    # Filter out players without the first and last name
    df_n = roster[(roster['First.Name'] == n[0]) & 
                  (roster['Last.Name'] == n[1])]
    
    # Append player id to list
    for player_id in df_n['Player.ID'].unique():
        id_list.append(player_id)

#%%
        
# LIST TO DATAFRAME
roster = pd.read_csv('roster2018.csv')

# List of lists of names [['first 1', 'last 1'], ['first 2', 'second 2'],...]
names = [['Albert', 'Pujols'], ['Mike', 'Trout'], ['David', 'Fletcher']]
  

df = pd.DataFrame(columns=['ID', 'Last', 'First'])
roster = roster.drop(columns=['Unnamed: 0', 'Bats', 'Pitches', 'Team', 'V7'])
roster.columns = ['ID', 'Last', 'First']
for n in names:
    # Filter out players with the first and last name
    df = df.append(roster[(roster['First'] == n[0]) &
                  (roster['Last'] == n[1])])
    
# reset index
df = df.reset_index(drop=True)

#%%

roster = pd.read_csv('roster2018.csv')

# List of lists of names [['first 1', 'last 1'], ['first 2', 'second 2'],...]

names = df.drop(columns=['ID'])
df = pd.DataFrame(columns=['ID', 'Last', 'First'])

# Iterate through all rows in names dataframe
for ix, row in names.iterrows():
    # Check if player's first and last name is in roster dataframe
    
    roster['match'] = roster['First.Name'].str.contains(row['First']) & \
                            roster['Last.Name'].str.contains(row['Last'])
                            
    # Get indexes of matches as np array
    player_ix = roster.index[roster.match]
    
    # For every match add to dataframe
    for i in player_ix:
        new_row = len(df)
        df.at[new_row, 'ID'] = roster.at[i, 'Player.ID']
        df.at[new_row, 'Last'] = roster.at[i, 'Last.Name']
        df.at[new_row, 'First'] = roster.at[i, 'First.Name']


#%%
# Initialize testing list to list
roster = pd.read_csv('roster2018.csv')
names = [['Albert', 'Pujols'], ['Mike', 'Trout'], ['David', 'Fletcher']]

from initialize_players import initialize_list_to_list

player = initialize_list_to_list(roster, names)


#%%
# Initialize testing LIST TO DATAFRAME
from initialize_players import initialize_list_to_df
df1 = initialize_list_to_df(roster, names)

#%% Initialize testing DF to DF
df_names = df1.drop(columns=['ID'])
from initialize_players import initialize_df_to_df
df2 = initialize_df_to_df(roster, df_names)






























