import pandas as pd

'''
Helper functions to get retrosheet player IDs from lists or dataframes of 
player names
'''

def initialize_list_to_list(roster, names):
    ''' Find player IDs for a list of players
    
    Arguments:
        roster: dataframe in retrosheet form
        names: list of lists containing first names and last names. List of 
                lists of names [['first 1', 'last 1'], 
                ['first 2', 'second 2'],...]       
        
    Output:
        player: list of lists of player IDs and names. In form of [['first 1', 
        'last 1', 'id 1', 'team 1'], ['first 2', 'last 2', 'id 2', 'team 2]]
    '''
    # Initialize id_list
    player = []
    
    # Find name matches
    for i, n in enumerate(names):
        df_n = roster[(roster['First.Name'] == n[0]) & 
                  (roster['Last.Name'] == n[1])]
        
        # Add ids, names, and teams to list
        for ix, row in df_n.iterrows():
            player.append([n[0], n[1], row['Player.ID'], row['Team']])
            
    return player
            
def initialize_list_to_df(roster, names):
    ''' Find player IDs for a list of players
    
    Arguments:
        roster: dataframe in retrosheet form
        names: list of lists containing first names and last names. List of 
                lists of names [['first 1', 'last 1'], 
                ['first 2', 'second 2'],...]       
        
    Output:
        df_player: dataframe with the columns 'ID', 'First', 'Last'
    '''
    # Initialize dataframe to be returned
    new_cols = ['ID', 'Last', 'First', 'Team']
    df_player = pd.DataFrame(columns=new_cols)
    
    # Clean roster dataframe to match column names
    roster = roster.drop(columns=['Unnamed: 0', 'Bats', 'Pitches', 'V7'])
    roster.columns = new_cols
    
    # Iterate through all the names in the lsits
    for n in names:
        # Filter out players with the first and last name
        df_player = df_player.append(roster[(roster['First'] == n[0]) &
                  (roster['Last'] == n[1])])
    
    # Reset index values and return
    return df_player.reset_index(drop=True)

def initialize_df_to_df(roster, names):
    ''' Find player IDs for a list of players
    
    Arguments:
        roster: dataframe in retrosheet form
        names: dataframe with the columns 'First' and 'Last'    
        
    Output:
        df_player: dataframe with the columns 'ID', 'First', 'Last'
    '''
    # Initialize dataframe to be returned
    new_cols = ['ID', 'Last', 'First', 'Team']
    df_player = pd.DataFrame(columns=new_cols)
    
    # Iterate through all rows in names dataframe
    for ix, row in names.iterrows():
        # Add column that checks if a the given player is in the roster df
        roster['match'] = roster['First.Name'].str.contains(row['First']) & \
                                roster['Last.Name'].str.contains(row['Last'])
                                
        # Get indexes of matches as numpy array
        player_ix = roster.index[roster.match]
        
        # For every match add to dataframe
        for i in player_ix:
            new_row = len(df_player)
            df_player.at[new_row, 'ID'] = roster.at[i, 'Player.ID']
            df_player.at[new_row, 'Last'] = roster.at[i, 'Last.Name']
            df_player.at[new_row, 'First'] = roster.at[i, 'First.Name']
            df_player.at[new_row, 'Team'] = roster.at[i, 'Team']
    
    return df_player