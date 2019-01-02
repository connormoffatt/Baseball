import pandas as pd
import numpy as np

def create_runs_matrix(pbp):
    ''' Solve for runs matrix (df) for base-out states given a set of
    retrosheet play-by-play data
    
    Argument: Retrosheet styple play by play data. Retrosheet data
    should have the given header fields given in the book Analyzing Baseball
    Data with R
    
    Output: dataframe containing value of each base out state given the
    play-by-play data    
    '''
    
    # First calculate the runs for a given play
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
    
    # Caclulate the numbe rof runs scored on each play
    pbp['runs_scored'] = (pbp.BAT_DEST_ID > 3).astype(int) + \
                                (pbp.RUN1_DEST_ID > 3).astype(int) + \
                                (pbp.RUN2_DEST_ID > 3).astype(int) + \
                                (pbp.RUN3_DEST_ID > 3).astype(int)
                                
    # Calculate Runs Value of each play
    pbp['runs_value'] = pbp.runs_new_state - pbp.runs_state + \
                                pbp.runs_scored

    return pbp

def create_standings(pbp):
    ''' Determine Win-Loss Records for each team given retrosheet play by play
    data. Teams must play a home game and an away game
    
    Argument: retrosheet play by play data
    
    Output: data frame containing team, wins, losses, win_pct
    '''
    
    # Initialize dataframe
    s = pd.DataFrame(columns=['W', 'L', 'home_wins', 'away_wins', 
                              'home_losses', 'away_losses', 'WPct'])

    # Determine whether the home team won for every game
    end = pbp[pbp.GAME_END_FL == 'T']
    
    # End of game score will be score before last play plus runs scored on 
    # last play
    end['away_final'] = end.AWAY_SCORE_CT
    end['home_final'] = end.HOME_SCORE_CT
    
    # Get the number of runs scored on the last play
    end['runs_scored'] = (end.BAT_DEST_ID > 3).astype(int) + \
                                (end.RUN1_DEST_ID > 3).astype(int) + \
                                (end.RUN2_DEST_ID > 3).astype(int) + \
                                (end.RUN3_DEST_ID > 3).astype(int)
                                
    # Add runs scored to home if BAT_HOME_ID is 1. otherwise add to away
    end['away_final'] = np.where(end.BAT_HOME_ID == 0, end.away_final + \
                           end.runs_scored, end.away_final)
    end['home_final'] = np.where(end.BAT_HOME_ID == 1, end.home_final + \
                           end.runs_scored, end.home_final)
    
    # Boolean for if the home team wins the game
    end['home_won'] = end.home_final > end.away_final
    
    # Get home team ID and away team id appended to year
    end['home'] = end.GAME_ID.str.slice(0, 7)
    end['away'] = end.AWAY_TEAM_ID + end.GAME_ID.str.slice(3, 7)
    
    # Get teams that had both a home and away game
    teams = set(end.home.append(end.away))
    
    # Iterate through all the teams to calculate s
    for t in teams:
        # Get results for home games
        s.at[t, 'home_wins'] = int(end[end.home == t].home_won.sum())
        s.at[t, 'away_wins'] = int((~end[end.away == t].home_won).sum())
        
        # Get rusults for away games
        s.at[t, 'home_losses'] = int((~end[end.home == t].home_won).sum())
        s.at[t, 'away_losses'] = int(end[end.away == t].home_won.sum())
        
        # Get total wins, losses, and winning %
        s.at[t, 'W'] = s.at[t, 'home_wins'] + s.at[t, 'away_wins']
        s.at[t, 'L'] = s.at[t, 'home_losses'] + s.at[t, 'away_losses']
        s.at[t, 'WPct'] = round(s.at[t, 'W'] / \
                            (s.at[t, 'W'] + s.at[t, 'L']), 3)
    
        # Get Runs Scored and Allowed
        s.at[t, 'R'] = int(end[end.home == t].home_final.sum() + \
                        end[end.away == t].away_final.sum())
        s.at[t, 'RA'] = int(end[end.home == t].away_final.sum() + \
                            end[end.away == t].home_final.sum())
                        
    return s  

def add_game_state(pbp, run_type='differential', standings=None):
    ''' Create a win probability matrix. Take take into account base, out,
    inning, and home-field advantage. Using actual score between home and away
    team. If model type is advanced take into account which team has a better
    record. standings data frame contains a team and their winning percentage 
    for a given season. Standings has index 'XXXYYY' where XXX is the team ID 
    and YYYY is the four digit year as index and an attribute for winning 
    percentage named 'WPct'
    
    Argument: 
        pbp: Retrosheet styple play by play data. 
        run_type: string that is either 'differential' or 'score. If it is
        'differential' our game state contains (Home Score - Away Score). If it
        is 'score' our game state contains Home Score + '_' + Away Score.
        standings: data frame containing WPct of teams being evaluated. If this
        is not None then team records will be taken into account.
    
    Output: data frame containing win probability of each state given the play 
    by play data. each state accounts for First Base Occupied, Second Base 
    Occupied, Third Base Occupied, Number of Outs, Inning, Home Score, 
    Away Score, or Differential
    '''
    
    # Get home and away winning percentage for each entry if using advanced
    # model
    if standings is not None:
        pbp['home'] = pbp.GAME_ID.str.slice(0, 7)
        pbp['away'] = pbp.AWAY_TEAM_ID + pbp.GAME_ID.str.slice(3, 7)
        pbp['home_WPct'] = standings.loc[pbp.home, 
                           'WPct'].fillna(0).reset_index(drop=True)
        pbp['away_WPct'] = standings.loc[pbp.away, 
                           'WPct'].fillna(0).reset_index(drop=True)
        pbp['home_better_WPct'] = pbp['home_WPct'] >= pbp['away_WPct']
        
        # drop derived columns
        pbp = pbp.drop(columns=['home', 'away', 'home_WPct', 'away_WPct'])
        
        # Get whether home or away has a better winning percentage
        pbp['better'] = np.where(pbp.home_better_WPct, 'H', 'A')
    
    # Get game-state for each play
    # (Run1)(Run2)(Run3)_(Outs)_(Inning)_(HomeScore)_(AwayScore)
    # Run is 1 or 0, Outs is 0,1,2, Inning T1 or B1, Home/Away Score run totals
    # and Potentially Home/Away better winning percentage, 'H' if home and 
    # 'A' if away
    
    # Get strings of 1 or 0 dependent if a base is occupied
    run1 = (~pbp.BASE1_RUN_ID.isna()).astype(int).astype(str)
    run2 = (~pbp.BASE2_RUN_ID.isna()).astype(int).astype(str)
    run3 = (~pbp.BASE3_RUN_ID.isna()).astype(int).astype(str)
    
    # Get inning
    inning = pbp.INN_CT.astype(str)
    pbp['half'] = np.where(pbp.BAT_HOME_ID == 0, 'T' + inning, 'B' + inning)
    
    # Get the beginning of the game state
    game_state_beg = run1 + run2 + run3 + '_' + pbp.OUTS_CT.astype(str) + \
                        '_' + pbp['half'] + '_'
                        
    # finish game state dependent on the run type
    if run_type == 'differential':
        game_state_end = (pbp.HOME_SCORE_CT - pbp.AWAY_SCORE_CT).astype(str)
    else:
        game_state_end =  pbp.HOME_SCORE_CT.astype(str) + '_' + \
                            pbp.AWAY_SCORE_CT.astype(str)
        
    pbp['game_state'] = game_state_beg + game_state_end
    
    # Add Better Winning Percentage if using advanced model
    if standings is not None:
        pbp['game_state'] += '_' + pbp.better
        
    return pbp
    
def add_home_won(pbp):
    ''' Add boolean to play by play data named 'home_won' that explains
    if the home team won the game
    
    Argument: retrosheet play by play data
    '''
    
    # First determine who wins the game
    end = pbp[pbp.GAME_END_FL == 'T']
    
    # End of game score will be score before last play plus runs scored on 
    # last play
    end['away_final'] = end.AWAY_SCORE_CT
    end['home_final'] = end.HOME_SCORE_CT
    
    # Get the number of runs scored on the last play
    end['runs_scored'] = (end.BAT_DEST_ID > 3).astype(int) + \
                                (end.RUN1_DEST_ID > 3).astype(int) + \
                                (end.RUN2_DEST_ID > 3).astype(int) + \
                                (end.RUN3_DEST_ID > 3).astype(int)
                                
    # Add runs scored to home if BAT_HOME_ID is 1. otherwise add to away
    end['away_final'] = np.where(end.BAT_HOME_ID == 0, end.away_final + \
                           end.runs_scored, end.away_final)
    end['home_final'] = np.where(end.BAT_HOME_ID == 1, end.home_final + \
                           end.runs_scored, end.home_final)
    
    # Boolean for if the home team wins the game
    end['home_won'] = end.home_final > end.away_final
    
    # Merge result with all play by play data
    end = end.loc[:, ['GAME_ID', 'home_won']]
    
    return pbp.merge(end)

#%%
def win_prob_matrix(pbp):
    ''' Create win probability matrix. There is the option to use run
    differential or actual score. There is also an optioon to account for 
    team's record. pbp data needs to  have the attribute 'home_win_prob' that
    gives the probability the home team will win for the given game-state. 
    pbp data also needs the attribute home_won. (i.e. the pbp data needs to 
    be ran through the functions add_home_won and add_game_state)
     
    
    Argument: 
        pbp: Retrosheet styple play by play data. Play by play data needs to
        have a 'game_state' as defined in previous functions and a 'home_won'
        attribute that is a boolean describing whether the home team won the
        game
    
    Output: data frame containing win probability of each state given the play 
    by play data. each state accounts for First Base Occupied, Second Base 
    Occupied, Third Base Occupied, Number of Outs, Inning, Home Score, 
    Away Score, or Differential
    '''

    # Calculate the win matrix
    win_matrix = pbp.loc[:, ['game_state', 'home_won']].groupby(
            ['game_state']).mean().loc[:, 'home_won']
    
    return win_matrix

#%%
    
def add_win_prob_value(pbp, win_matrix):
    ''' Determine impact on win probability for each play. pbp data needs to
    have the attribute 'home_win_prob' that gives the probability the home
    team will win for the given game-state. pbp data also needs the attribute
    home_won. (i.e. the pbp data needs to be ran through the functions
    add_home_won and add_game_state)
     
    Argument: 
       pbp: Retrosheet styple play by play data. Needs to contain
       win_matrix: win probability of home team for given game states
        
    Output: play by play data with a new attribute 'win_value' that gives the
    increase or decrease in win probability for a given play
    '''
    
    # Get the home winning probability for a given state
    pbp['home_win_prob'] = win_matrix.loc[pbp.game_state,
                           ].reset_index(drop=True)
    
    # reset index before looping
    pbp = pbp.reset_index(drop=True)
    
    # Loop through the first len(pbp) - 1 rows 
    for ix, row in pbp.loc[:len(pbp) - 2,].iterrows():
        # set new_home_win_prob equal to the new_home_win_prob of the next play
        pbp.at[ix, 'new_home_win_prob'] = pbp.at[ix + 1, 'home_win_prob']
        
    # Loop through all plays that are the end of a game and set the new win
    # probability to home_won
    for ix in pbp[pbp.GAME_END_FL == 'T'].index:
        pbp.at[ix, 'new_home_win_prob'] = pbp.at[ix, 'home_won'].astype(int)

    # Get the value of each play
    pbp['win_value'] = pbp.new_home_win_prob - pbp.home_win_prob
    
    return pbp
    