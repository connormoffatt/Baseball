import pandas as pd

def create_runs_matrix(pbp):
    ''' Solve for runs matrix (df) for base-out states given a set of
    retrosheet play-by-play data
    
    Argument: Retrosheet styple play by play data. Retrosheet data
    should have the given header fields given in the book Analyzing Baseball
    Data with R
    
    Output: dataframe containing value of each base out state given the
    play-by-play data    
    '''
    
    # First calculate the runs at a given time
    pbp['RUNS'] = pbp.AWAY_SCORE_CT + pbp.HOME_SCORE_CT
    
    # Create a unique ID for each half inning
    pbp['HALF_INNING'] = pbp.GAME_ID + pbp.INN_CT.map(str) + \
                                pbp.BAT_HOME_ID.map(str)
    
    # Now we will calculate how many runs were scored at the end of the inning
    
    # Calculate the number of runs scored during each play
    pbp['RUNS_SCORED'] = (pbp.BAT_DEST_ID > 3).astype(int) + \
                                (pbp.RUN1_DEST_ID > 3).astype(int) + \
                                (pbp.RUN2_DEST_ID > 3).astype(int) + \
                                (pbp.RUN3_DEST_ID > 3).astype(int)
    
    # Get the Number of runs scored in a specific inning
    RUNS_SCORED_INNING = pbp.groupby(['HALF_INNING']).sum().loc[:, 
                                         'RUNS_SCORED']
    
    # Find the total game runs at the beginning of the inning with '[' function 
    RUNS_SCORED_START = pbp.loc[:, ['HALF_INNING', 'RUNS']].groupby(
            ['HALF_INNING']).min().loc[:, 'RUNS']
    
    # Get the maximum number of runs in the half inning
    MAX = pd.DataFrame(RUNS_SCORED_INNING + RUNS_SCORED_START)
    MAX.columns = ['MAX_RUNS']
    MAX['half'] = MAX.index
    
    # Merge together the max_runs into the pbp dataframe
    pbp = pbp.merge(MAX, left_on='HALF_INNING', right_on='half')
    
    # Calculate the runs for the remainder of the inning. Typo in Book
    pbp['RUNS_ROI'] = pbp.MAX_RUNS - pbp.RUNS
    
    # Create Binary Variable to determine if runner is on a base before play
    RUNNER1 = pbp['BASE1_RUN_ID'].notna().astype(int)
    RUNNER2 = pbp['BASE2_RUN_ID'].notna().astype(int)
    RUNNER3 = pbp['BASE3_RUN_ID'].notna().astype(int)
    
    # Create the current state 
    pbp['state'] = RUNNER1.map(str) + RUNNER2.map(str) + RUNNER3.map(str) + \
                        ' ' + pbp.OUTS_CT.map(str)
    
    # Create Binary Variable to determine if a runner is on a base after play
    NRUNNER1 = ((pbp.RUN1_DEST_ID == 1) | \
                (pbp.BAT_DEST_ID == 1)).astype(int)
    
    NRUNNER2 = ((pbp.BAT_DEST_ID == 2) | \
                (pbp.RUN1_DEST_ID == 2) | \
                (pbp.RUN2_DEST_ID == 2)).astype(int)
    
    NRUNNER3 = ((pbp.BAT_DEST_ID == 3) | \
                (pbp.RUN1_DEST_ID == 3) | \
                (pbp.RUN2_DEST_ID == 3) | \
                (pbp.RUN3_DEST_ID == 3)).astype(int)
    
    # Get number of outs at the end of play
    NOUTS = pbp.OUTS_CT + pbp.EVENT_OUTS_CT
    
    # Get the new state at the end of the play
    pbp['new_state'] = NRUNNER1.map(str) + NRUNNER2.map(str) + \
                            NRUNNER3.map(str) + ' ' + NOUTS.map(str)
    
    # Reduce dataframe to when states change or runs score
    pbp = pbp[(pbp.state != pbp.new_state) | 
                (pbp.RUNS_SCORED > 0)]
    
    # Get the number of outs per inning and merge into the dataframe
    OUTS = pd.DataFrame(pbp.loc[:, ['HALF_INNING', 'EVENT_OUTS_CT']].groupby(
            ['HALF_INNING']).sum().loc[:, 'EVENT_OUTS_CT'])
    OUTS.columns = ['INNING_OUTS']
    OUTS['half'] = OUTS.index
    pbp = pbp.merge(OUTS, left_on='HALF_INNING', right_on='half')
    
    # filter out half innings that are walk-offs because they are not complete
    # innings
    pbpc = pbp[pbp.INNING_OUTS == 3]
    
    # Calculate the expected number of runs for each element of the matrix
    RUNS = pd.DataFrame(pbpc.loc[:, ['state', 'RUNS_ROI']].groupby(
            ['state']).mean().loc[:, 'RUNS_ROI'])
    
    s3 = ['000 3', '001 3', '010 3', '011 3', '100 3', '101 3', '110 3', 
          '111 3']
    zeros_data = {'RUNS_ROI':[0,0,0,0,0,0,0,0]}
    
    run_matrix = RUNS.append(pd.DataFrame(data=zeros_data, index=s3))
    
    return run_matrix

def add_runs_value(pbp, run_matrix):
    ''' Add runs value for each play to the play by play dataframe. Other 
    columns added are STATE, new_state, runs_state, runs_new_state
    
    STATE: state before play of three 1/0 for whether a runner is on a base 
    followed by a space and then the out total. 110 2 is runners on 1st and 
    2nd with 2 outs
    
    new_state: state after play
    
    runs_state: expected number of runs in given base-out state before play
    
    runs_new_state: expected number of runs in given base-out state after play
    
    runs_value: difference between runs_new_state and runs_state
    
    Arguments:
            pbp: retrosheet play by play data
            run_matrix: dataframe containing all of the base-out states and
            their value according to a set of play by play data
    
    Output:
        Retrosheet styple play by play data. Retrosheet data
    should have the given header fields given in the book Analyzing Baseball
    Data with R
    '''
    
    # Initialize columns to delete before returning dataframe
    
    # First calculate the
    # Create Binary Variable to determine if runner is on a base before play
    RUNNER1 = pbp['BASE1_RUN_ID'].notna().astype(int)
    RUNNER2 = pbp['BASE2_RUN_ID'].notna().astype(int)
    RUNNER3 = pbp['BASE3_RUN_ID'].notna().astype(int)
    
    # Create the current state 
    pbp['state'] = RUNNER1.map(str) + RUNNER2.map(str) + RUNNER3.map(str) + \
                        ' ' + pbp.OUTS_CT.map(str)
    
    # Create Binary Variable to determine if a runner is on a base after play
    NRUNNER1 = ((pbp.RUN1_DEST_ID == 1) | \
                (pbp.BAT_DEST_ID == 1)).astype(int)
    
    NRUNNER2 = ((pbp.BAT_DEST_ID == 2) | \
                (pbp.RUN1_DEST_ID == 2) | \
                (pbp.RUN2_DEST_ID == 2)).astype(int)
    
    NRUNNER3 = ((pbp.BAT_DEST_ID == 3) | \
                (pbp.RUN1_DEST_ID == 3) | \
                (pbp.RUN2_DEST_ID == 3) | \
                (pbp.RUN3_DEST_ID == 3)).astype(int)
    
    # Get number of outs at the end of play
    NOUTS = pbp.OUTS_CT + pbp.EVENT_OUTS_CT
    
    # Get the new state at the end of the play
    pbp['new_state'] = NRUNNER1.map(str) + NRUNNER2.map(str) + \
                            NRUNNER3.map(str) + ' ' + NOUTS.map(str)
        
    # Calculate Runs Value of State Before Play
    pbp['runs_state'] = run_matrix.loc[pbp.state,].reset_index().loc[:,
                           'RUNS_ROI']
    
    # Calculate Runs Value of State After Play
    pbp['runs_new_state'] = run_matrix.loc[pbp.
                                    new_state,].reset_index().loc[:,'RUNS_ROI']
    
    # Calculate Runs Value of each play
    pbp['runs_value'] = pbp.runs_new_state - pbp.runs_state + \
                                pbp.RUNS_SCORED
                                
    # Caclulate the numbe rof runs scored on each play
    pbp['runs_scored'] = (pbp.BAT_DEST_ID > 3).astype(int) + \
                                (pbp.RUN1_DEST_ID > 3).astype(int) + \
                                (pbp.RUN2_DEST_ID > 3).astype(int) + \
                                (pbp.RUN3_DEST_ID > 3).astype(int)

    return pbp