import pandas as pd
from general import retrosheet_event_dict

def get_positions(players, pbp):
    ''' For each player, determine the positions that they played during the
    play by play data
    
    Arguments:
        players: dataframe containing retrosheet player id's with the attribute
                named "ID"
        pbp: retrosheet play by play data
        
    Output: dataframe containing player ID and positions they played in the
            play by play data. Note: players can have multiple entries
    '''
    position = pd.DataFrame()
    
    # Merge Pitchers
    pitcher = pd.DataFrame(data=pbp.RESP_PIT_ID.unique(), columns=['ID'])
    pitcher['position'] = 1
    players1 = players.merge(pitcher, how='left', on='ID')
    position = position.append(players1[~players1.position.isna()])
    
    
    # Merge Catchers
    catcher = pd.DataFrame(data=pbp.POS2_FLD_ID.unique(), columns=['ID'])
    catcher['position'] = 2
    players2 = players.merge(catcher, how='left', on='ID')
    position = position.append(players2[~players2.position.isna()])
    
    # Merge First basemen
    first = pd.DataFrame(data=pbp.POS3_FLD_ID.unique(), columns=['ID'])
    first['position'] = 3
    players3 = players.merge(first, how='left', on='ID')
    position = position.append(players3[~players3.position.isna()])
    
    # Merge Second basemen
    second = pd.DataFrame(data=pbp.POS4_FLD_ID.unique(), columns=['ID'])
    second['position'] = 4
    players4 = players.merge(second, how='left', on='ID')
    position = position.append(players4[~players4.position.isna()])
    
    # Merge Short
    short = pd.DataFrame(data=pbp.POS6_FLD_ID.unique(), columns=['ID'])
    short['position'] = 6
    players6 = players.merge(short, how='left', on='ID')
    position = position.append(players6[~players6.position.isna()])
    
    # Merge Third
    third = pd.DataFrame(data=pbp.POS6_FLD_ID.unique(), columns=['ID'])
    third['position'] = 5
    players5 = players.merge(third, how='left', on='ID')
    position = position.append(players5[~players5.position.isna()])
    
    # Merge Left
    left = pd.DataFrame(data=pbp.POS7_FLD_ID.unique(), columns=['ID'])
    left['position'] = 7
    players7 = players.merge(left, how='left', on='ID')
    position = position.append(players7[~players7.position.isna()])
    
    # Merge Center
    center = pd.DataFrame(data=pbp.POS8_FLD_ID.unique(), columns=['ID'])
    center['position'] = 8
    players8 = players.merge(center, how='left', on='ID')
    position = position.append(players8[~players8.position.isna()])
    
    # Merge Right
    right = pd.DataFrame(data=pbp.POS9_FLD_ID.unique(), columns=['ID'])
    right['position'] = 9
    players9 = players.merge(right, how='left', on='ID')
    position = position.append(players9[~players9.position.isna()])
    
    # Reset index and sort by id and position
    position = position.sort_values(by=['ID', 'position'])
    position = position.reset_index(drop=True)
    
    return position

def sort_by_position_and_player(pbp, pid, pos):
    ''' Reduce play by play data to plays where a single player is playing a 
    specific position
    
    Argument:
        pbp: retrosheet play by play data
        pid: retrosheet player ID
        pos: player's position 1-9
        
    Output: The dataframe reduced by position and player
    '''

    # Reduce dataframe to when player is playing the given position
    if pos == 1:
        p = pbp[pbp.RESP_PIT_ID == pid]
    elif pos == 2:
        p = pbp[pbp.POS2_FLD_ID == pid]
    elif pos == 3:
        p = pbp[pbp.POS3_FLD_ID == pid]
    elif pos == 4:
        p = pbp[pbp.POS4_FLD_ID == pid]
    elif pos == 5:
        p = pbp[pbp.POS5_FLD_ID == pid]
    elif pos == 6:
        p = pbp[pbp.POS6_FLD_ID == pid]
    elif pos == 7:
        p = pbp[pbp.POS7_FLD_ID == pid]
    elif pos == 8:
        p = pbp[pbp.POS8_FLD_ID == pid]
    elif pos == 9:
        p = pbp[pbp.POS9_FLD_ID == pid]
    return p

def standard_fielding(pbp, df):
    ''' Add all standard fielding statistics to a dataframe
    
    Standard Stats: 'G', 'GS', 'Inn', 'PO', 'A', 'E', 'FE', 'TE', 'DP', 'DPS', 
                    'DPT', 'DPF', 'SB', 'CS', 'PB', 'WP', 'FP'
    
    Note: DP(S/T/F) -> double plays started/turned/fielded
    
    Arguments:
        pbp: play by play data for a given period. 
        df: dataframe with players to calculate standard statistics for
        
    Output:
        dataframe with standard stats appended
    '''
    # create event dictionary
    e = retrosheet_event_dict()
    
    # iterate through every player in the dataframe
    for ix, row in df.iterrows():
        
        # Get player id and position for the current row
        pid = row['ID']
        pos = row['position']
        
        # Get play by play where player is at the given position
        
        p = sort_by_position_and_player(pbp, pid, pos)
        
        # Games
        df.at[ix, 'G'] = len(p.GAME_ID.unique())
        
        # Games Started. Assume no substutions 0 outs in first innin
        p_start = p[(p.INN_CT == 1) & (p.OUTS_CT == 0)]
        df.at[ix, 'GS'] = len(p_start.GAME_ID.unique())
        
        # Innings
        p['inning'] = p['GAME_ID'] + p['INN_CT'].astype(str)
        df.at[ix, 'Inn'] = len(p.inning.unique())
        
        # Put Outs
        df.at[ix, 'PO'] = len(p[p.PO1_FLD_CD == pos]) + \
            len(p[p.PO2_FLD_CD == pos]) + len(p[p.PO3_FLD_CD == pos])
            
        # Assists
        df.at[ix, 'A'] = len(p[p.ASS1_FLD_CD == pos]) + \
            len(p[p.ASS2_FLD_CD == pos]) + len(p[p.ASS3_FLD_CD == pos]) + \
            len(p[p.ASS4_FLD_CD == pos]) + len(p[p.ASS5_FLD_CD == pos])
            
        # Errors
        df.at[ix, 'E'] = len(p[p.ERR1_FLD_CD == pos]) + \
            len(p[p.ERR2_FLD_CD == pos]) + len(p[p.ERR3_FLD_CD == pos])
        
        # Fielding Errors
        df.at[ix,'FE'] = len((p[p.ERR1_FLD_CD== pos]) & (p[p.ERR1_CD== 'F']))
        df.at[ix,'FE'] += len((p[p.ERR2_FLD_CD== pos]) & (p[p.ERR2_CD== 'F']))
        df.at[ix,'FE'] += len((p[p.ERR3_FLD_CD== pos]) & (p[p.ERR3_CD== 'F']))
             
        # Throwing Errors
        df.at[ix,'TE'] = len((p[p.ERR1_FLD_CD== pos]) & (p[p.ERR1_CD== 'T']))
        df.at[ix,'TE'] += len((p[p.ERR2_FLD_CD== pos]) & (p[p.ERR2_CD== 'T']))
        df.at[ix,'TE'] += len((p[p.ERR3_FLD_CD== pos]) & (p[p.ERR3_CD== 'T']))
            
        # Double Plays
        dp = p[p.DP_FL == 'T']
        df.at[ix, 'DP'] = len(dp[(dp.PO1_FLD_CD == pos) | \
                                    (dp.PO2_FLD_CD == pos) | \
                                    (dp.PO3_FLD_CD == pos) | \
                                    (dp.ASS1_FLD_CD == pos) | \
                                    (dp.ASS2_FLD_CD == pos) | \
                                    (dp.ASS3_FLD_CD == pos) | \
                                    (dp.ASS4_FLD_CD == pos) | \
                                    (dp.ASS5_FLD_CD == pos)])
        
        # Double Plays Started (Only account for ground ball double plays)
        df.at[ix, 'DPS'] = len(dp[(dp.BATTEDBALL_CD == 'G') & \
                                 (dp.PO1_FLD_CD == pos)])
    
        # Double Plays Turned (Only account for ground ball double plays)
        df.at[ix, 'DPT'] = len(dp[(dp.BATTEDBALL_CD == 'G') & \
                                 (dp.ASS1_FLD_CD == pos)])
    
        # Double Plays Fieleded (Only account for ground ball double plays)
        df.at[ix, 'DPF'] = len(dp[(dp.BATTEDBALL_CD == 'G') & \
                                 (dp.PO2_FLD_CD == pos)])
    
        # Pitcher/Catcher Statistics
        if pos == 1 or pos == 2:
            # Stolen Bases
            df.at[ix, 'SB'] = p[p.EVENT_CD == e['Stolen Base']]
            
            # Caught Stealing
            df.at[ix, 'CS'] = p[p.EVENT_CD == e['Caught stealing']]
            
            # Passed Ball
            df.at[ix, 'PB'] = p[p.EVENT_CD == e['Passed ball']]
            
            # Wild Pitches
            df.at[ix, 'WP'] = p[p.EVENT_CD == e['Wild pitch']]
            
             # Convert correct column types to int
            int_cols = ['SB', 'CS', 'PB', 'WP']
            
            for col in int_cols:
                df[col] = df[col].astype(int)
            
        # Fielding Percentage
        df.at[ix, 'FP'] = df.at[ix, 'PO'] + df.at[ix, 'A']
        df.at[ix, 'FP'] = df.at[ix, 'FP'] / (df.at[ix, 'FP'] + df.at[ix, 'E'])
        
    # Convert correct column types to int
    int_cols = ['G', 'GS', 'Inn', 'PO', 'A', 'E', 'FE', 'TE', 'DP', 'DPS',
                'DPT', 'DPF']
    
    for col in int_cols:
        df[col] = df[col].astype(int)
    
    return df

def total_fielding(df):
    ''' Total fielding statistics across all positions for each player
    
    Argument: df containing fielding statistics. Must have 'ID' column giving
    retrosheete player IDs
    
    Output: fielding statistic totals data frame
    '''
    return

def advanced_fielding(pbp, df):
    ''' Add all advanced fielding statistics to a dataframe
    
    Note: We will only calculate select modified versions of fielding
    statistics for simplicity
    
    Advanced Stats: 
    
    Arguments:
        pbp: play by play data for a given period. 
        df: dataframe with players to calculate standard statistics for
        
    Output:
        dataframe with advanced stats appended
    '''









