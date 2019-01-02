import pandas as pd
import numpy as np

from general import add_runs_value
from general import create_runs_matrix
from general import add_home_won
from general import add_game_state
from general import win_prob_matrix
from general import add_win_prob_value
from general import create_standings

import warnings
warnings.filterwarnings('ignore')

#%%

def retrosheet_event_dict():
    ''' create and return retrosheet event dictionary'''
    d = {}
    d['Unknown Event'] = 0
    d['No event'] = 1
    d['Generic out'] = 2
    d['Strikeout'] = 3
    d['Stolen base'] = 4
    d['Defensive indifference'] = 5
    d['Caught stealing'] = 6
    d['Pickoff error'] = 7
    d['Pickoff'] = 8
    d['Wild pitch'] = 9
    d['Passed ball'] = 10
    d['Balk'] = 11
    d['Other Advance'] = 12
    d['Foul error'] = 13
    d['Walk'] = 14
    d['Intentional walk'] = 15
    d['Hit by pitch'] = 16
    d['Interference'] = 17
    d['Error'] = 18
    d['Fielder choice'] = 19
    d['Single'] = 20
    d['Double'] = 21
    d['Triple'] = 22
    d['Home run'] = 23
    d['Missing play'] = 24
    return d

def standard_batting(pbp, df):
    ''' Add all standard batting statistics to a dataframe
    
    Standard Stats: 'G', 'AB', 'PA', 'H', '1B', '2B', '3B', 'HR', 'R', 'RBI',
                    'BB', 'IBB', 'SO', 'HBP', 'SF', 'SH', 'GDP', 'SB', 'CS'
    
    Arguments:
        pbp: play by play data for a given period
        df: dataframe with players to calculate standard statistics for
        
    Output:
        dataframe with standard stats appended
    '''
    # create event dictionary
    e = retrosheet_event_dict()
    
    # iterate through every player in the dataframe
    for ix, row in df.iterrows():
        
        # Get player id for the current row
        pid = row['ID']
        
        # Get dataframe while player id the batter during a batting event
        df_bat = pbp[(pbp.RESP_BAT_ID == pid) & (pbp.BAT_EVENT_FL == 'T')]
    
        # GAMES
        # Original Batter, Responsible Batter, On Base, Playing a Position
        
        # Get all plays if player was in a game
        pbp_played = pbp[(pbp.BAT_ID == pid) | (pbp.RESP_BAT_ID == pid) |
                        (pbp.PIT_ID == pid) | (pbp.RESP_PIT_ID == pid) |
                        (pbp.BASE1_RUN_ID == pid) | (pbp.BASE2_RUN_ID == pid) |
                        (pbp.BASE3_RUN_ID == pid) | (pbp.POS2_FLD_ID == pid) |
                        (pbp.POS3_FLD_ID == pid) | (pbp.POS4_FLD_ID == pid) |
                        (pbp.POS5_FLD_ID == pid) | (pbp.POS6_FLD_ID == pid) |
                        (pbp.POS7_FLD_ID == pid) | (pbp.POS8_FLD_ID == pid) |
                        (pbp.POS9_FLD_ID == pid) ]
        df.at[ix, 'G'] = len(pbp_played.GAME_ID.unique())
        
        # PLATE APPEARANCES
        df.at[ix, 'PA'] = len(df_bat)
        
        # HITS
        hits = [e['Single'], e['Double'], e['Triple'], e['Home run']]
        df.at[ix, 'H'] = (df_bat.EVENT_CD.isin(hits)).sum()
        
        # SINGLES
        df.at[ix, '1B'] = (df_bat.EVENT_CD == e['Single']).sum()
        
        # DOUBLES
        df.at[ix, '2B'] = (df_bat.EVENT_CD == e['Double']).sum()
        
        # TRIPLES
        df.at[ix, '3B'] = (df_bat.EVENT_CD == e['Triple']).sum()
        
        # HOME RUNS
        df.at[ix, 'HR'] = (df_bat.EVENT_CD == e['Home run']).sum()
        
        # RUNS
        
        # Calculate whether each runner ends at home plate
        # run destination 4: earned, 5: unearned, 6: team unearned
        runs1 = ((pbp.BASE1_RUN_ID == pid) & (pbp.RUN1_DEST_ID > 3)).sum()
        runs2 = ((pbp.BASE2_RUN_ID == pid) & (pbp.RUN2_DEST_ID > 3)).sum()
        runs3 = ((pbp.BASE3_RUN_ID == pid) & (pbp.RUN3_DEST_ID > 3)).sum()
        runs4 = ((pbp.RESP_BAT_ID == pid) & (pbp.BAT_DEST_ID > 3)).sum()
        df.at[ix, 'R'] = runs1 + runs2 + runs3 + runs4

        # RBI
        df.at[ix, 'RBI'] = df_bat.RBI_CT.sum()
        
        # BB
        df.at[ix, 'BB'] = (df_bat.EVENT_CD == e['Walk']).sum()
        
        # IBB
        df.at[ix, 'IBB'] = (df_bat.EVENT_CD == e['Intentional walk']).sum()
        
        # SO
        df.at[ix, 'SO'] = (df_bat.EVENT_CD == e['Strikeout']).sum()
        
        # HBP
        df.at[ix, 'HBP'] = (df_bat.EVENT_CD == e['Hit by pitch']).sum()
        
        # SF
        df.at[ix, 'SF'] = (df_bat.SF_FL == 'T').sum()
        
        # SH
        df.at[ix, 'SH'] = (df_bat.SH_FL == 'T').sum()
        
        # GDP
        df.at[ix, 'GDP'] = ((df_bat.BATTEDBALL_CD == 'G') & \
                             (df_bat.DP_FL == 'T')).sum()
        
        # SB
        # Sum stolen base at each base
        sb1 = ((pbp.BASE1_RUN_ID == pid) & (pbp.RUN1_SB_FL == 'T')).sum()
        sb2 = ((pbp.BASE2_RUN_ID == pid) & (pbp.RUN2_SB_FL == 'T')).sum()
        sb3 = ((pbp.BASE3_RUN_ID == pid) & (pbp.RUN3_SB_FL == 'T')).sum()
        df.at[ix, 'SB'] = sb1 + sb2 + sb3
            
        # CS
        # Sum caught stealing at each base
        cs1 = ((pbp.BASE1_RUN_ID == pid) & (pbp.RUN1_CS_FL == 'T')).sum()
        cs2 = ((pbp.BASE2_RUN_ID == pid) & (pbp.RUN2_CS_FL == 'T')).sum()
        cs3 = ((pbp.BASE3_RUN_ID == pid) & (pbp.RUN3_CS_FL == 'T')).sum()
        df.at[ix, 'CS'] = cs1 + cs2 + cs3

        # At Bats
        at_bat = hits + [e['Generic out'], e['Strikeout'], e['Error'],
                         e['Fielder choice']]
        
        # Sum of hits, outs, errors, and fielders choice minus sacrifices
        df.at[ix, 'AB'] = (df_bat.EVENT_CD.isin(at_bat)).sum() - \
                            df.at[ix, 'SF'] - df.at[ix, 'SH']
        
        # Average
        df.at[ix, 'AVG'] = round(df.at[ix, 'H'] / df.at[ix, 'AB'], 3)
        
    # Convert correct column types to int
    int_cols = ['G', 'AB', 'PA', 'H', '1B', '2B', '3B', 'HR', 'R', 'RBI',
                'BB', 'IBB', 'SO', 'HBP', 'SF', 'SH', 'GDP', 'SB', 'CS']
    
    for col in int_cols:
        df[col] = df[col].astype(int)
    
    return df

def double_play_run_values(pbp):
    ''' Calculate runs values for eight different base-out states for 
    double play opportunities
    
        Argument: 
            retrosheet play by play data
        
        Output:
            dictionary containing run values for double play opporuntiies
    '''
    # Filter play by play into events that are double play opportunities
    # Fielder's choices and double plays
    
    e = retrosheet_event_dict()
    
    pbp_dp = pbp[(pbp.BATTEDBALL_CD == 'G') & ((pbp.DP_FL == 'T') | \
                 (pbp.EVENT_CD == e['Fielder choice']))]
        
    # initialize dictaionry to be returned with dp runs values
    d = {}
        
    # We simply find the mean of the runs value because that will equally
    # weight the run value oof each event
    
    # Value for runners on second and third
    d['100 0'] = pbp_dp[pbp_dp.state == '100 0'].runs_value.mean()
    d['100 1'] = pbp_dp[pbp_dp.state == '100 1'].runs_value.mean()
    
    # Value for runners on first and second
    d['110 0'] = pbp_dp[pbp_dp.state == '110 0'].runs_value.mean()
    d['110 1'] = pbp_dp[pbp_dp.state == '110 1'].runs_value.mean()
    
    # Value for runners bases loaded
    d['111 0'] = pbp_dp[pbp_dp.state == '111 0'].runs_value.mean()
    d['111 1'] = pbp_dp[pbp_dp.state == '111 1'].runs_value.mean()
    
    # Value for runners on first and third. Also filter out plays at home
    d['101 0'] = pbp_dp[(pbp_dp.state == '101 0') & (pbp_dp.RUN3_DEST_ID < 4) \
                          & (pbp_dp.RUN3_PLAY_TX.isna())].runs_value.mean()
    d['101 1'] = pbp_dp[(pbp_dp.state == '101 1') & (pbp_dp.RUN3_DEST_ID < 4) \
                          & (pbp_dp.RUN3_PLAY_TX.isna())].runs_value.mean()
    
    return d

def wGDP_score(pbp, pid, dp_avg_runs):
    ''' Calculate a players wGDP value
    
    Arguments:
        df_bat: play by play data filtered such that a specific player is
        the responsible batter for
        pbp: retrosheet play by play data
        pid: player ID for the 
        dp_avg_runs: Average run values for various double play opportunities
    
    Output:
        wGDP value f or a given player    
    '''
    e = retrosheet_event_dict()
    df_bat = pbp[(pbp.RESP_BAT_ID == pid) & (pbp.BAT_EVENT_FL == 'T')]
    
    # Get double play weights for the batter
    df_bat_dp = df_bat[(df_bat.BATTEDBALL_CD == 'G') & 
                       ((df_bat.DP_FL == 'T') | 
                       (df_bat.EVENT_CD == e['Fielder choice']))]
    
    # Total value for runner on first
    dp_100_0_val = (df_bat_dp[df_bat_dp.state == '100 0'].runs_value - 
                    dp_avg_runs['100 0']).sum()
    dp_100_1_val = (df_bat_dp[df_bat_dp.state == '100 1'].runs_value - 
                    dp_avg_runs['100 1']).sum()
    
    # Total value for runner on first and second
    dp_110_0_val = (df_bat_dp[df_bat_dp.state == '110 0'].runs_value - 
                    dp_avg_runs['110 0']).sum()
    dp_110_1_val = (df_bat_dp[df_bat_dp.state == '110 1'].runs_value - 
                    dp_avg_runs['110 1']).sum()
    
    # Total value for bases loaded
    dp_111_0_val = (df_bat_dp[df_bat_dp.state == '111 0'].runs_value - 
                    dp_avg_runs['111 0']).sum()
    dp_111_1_val = (df_bat_dp[df_bat_dp.state == '111 1'].runs_value - 
                    dp_avg_runs['111 1']).sum()
    
    # Total value for first and third
    dp_101_0_val = (df_bat_dp[(df_bat_dp.state == '101 0') & \
                              (df_bat.RUN3_DEST_ID < 4) & \
                              (df_bat_dp.RUN3_PLAY_TX.isna())].runs_value 
                              - dp_avg_runs['101 0']).sum()
    dp_101_1_val = (df_bat_dp[(df_bat_dp.state == '101 1') & \
                              (df_bat.RUN3_DEST_ID < 4) & \
                              (df_bat_dp.RUN3_PLAY_TX.isna())].runs_value 
                              - dp_avg_runs['101 1']).sum()
    
    # Sum total value and return    
    wGDP = dp_100_0_val + dp_100_1_val + dp_110_0_val + dp_110_1_val + \
            dp_111_0_val + dp_111_1_val + dp_101_0_val + dp_101_1_val
            
    return wGDP
        
    
def ubr_run_frequency(pbp):
    ''' Calculate frequency of baserunning events from play by play data
    
    Arguments:
        pbp: retrosheet play-by-play data to calculate frequency of events from
    
    Output:
        Dictionary that determines frequency for which baserunning events
        such as a batter advancing occurs
    '''
    # Initialize retrosheet events
    e = retrosheet_event_dict()
    
    # Initilaize output dictionary that will contain frequencies of events
    d = {}
        
    # Calculation does not account for when runners do not move up one base
    # on singles and two bases on double. Also assumes that runners will not
    # score from first on singles
    
    # Type (1) Players advance extra base on bases
    
    # Create dataframe for when there is a runner on first and a runner
    # does not end up on third. For singles and doubles
    df1s = pbp[(~pbp.BASE1_RUN_ID.isna()) & (pbp.EVENT_CD == e['Single']) & \
               (pbp.RUN3_DEST_ID != 3) & (pbp.RUN2_DEST_ID != 3)]
    df1d = pbp[(~pbp.BASE1_RUN_ID.isna()) & (pbp.EVENT_CD == e['Double'])]
    
    # Create dataframe for when there is a runner on second and a single
    df2s = pbp[(~pbp.BASE2_RUN_ID.isna()) & (pbp.EVENT_CD == e['Single'])]
    
    # 1s means single with runner on first 1d is double with runner on first
    # 2s means single with runner on second
    
    # Get the frequency for staying, or out for the runner on first when
    # they are not blocked
    d['1s_advance'] = len(df1s[df1s.RUN1_DEST_ID == 3])
    d['1s_stay'] = len(df1s[df1s.RUN1_DEST_ID == 2])
    d['1s_out'] = len(df1s[(df1s.RUN1_DEST_ID == 0) & \
                     (~df1s.RUN1_PLAY_TX.isna())])
    
    # normalize runner on first single
    first_single = d['1s_advance'] + d['1s_stay'] + d['1s_out']
    d['1s_advance'] = d['1s_advance'] / first_single
    d['1s_stay'] = d['1s_stay'] / first_single
    d['1s_out'] = d['1s_out'] / first_single
    
    # Get the frequency for staying, advance, or out for the runner on first
    # during a double
    d['1d_advance'] = len(df1d[df1d.RUN1_DEST_ID >= 4])
    d['1d_stay'] = len(df1d[df1d.RUN1_DEST_ID == 3])
    d['1d_out'] = len(df1d[(df1d.RUN1_DEST_ID == 0) & \
                         (~df1d.RUN1_PLAY_TX.isna())])
    
    # normalize runner on first double
    first_double = d['1d_advance'] + d['1d_stay'] + d['1d_out']
    d['1d_advance'] = d['1d_advance'] / first_double
    d['1d_stay'] = d['1d_stay'] / first_double
    d['1d_out'] = d['1d_out'] / first_double
    
    # Get the frequency for staying, advancing, or out for runner on second
    # during a single
    d['2s_advance'] = len(df2s[df2s.RUN2_DEST_ID == 4])
    d['2s_stay'] = len(df2s[df2s.RUN2_DEST_ID == 3])
    d['2s_out'] = len(df2s[(df2s.RUN2_DEST_ID == 0) & \
                     (~df2s.RUN2_PLAY_TX.isna())]) 

    # normalize runner on second single
    second_single = d['2s_advance'] + d['2s_stay'] + d['2s_out']
    d['2s_advance'] = d['2s_advance'] / second_single
    d['2s_stay'] = d['2s_stay'] / second_single
    d['2s_out'] = d['2s_out'] / second_single
    
    # Type (2) Batters Advancing an extra base
    # Assume that batters do not extend triples for inside the park home run
    
    # Get singles where runner is not blocked
    df0s = pbp[(pbp.EVENT_CD == e['Single']) & (pbp.RUN1_DEST_ID != 2)]
    
    # Get doubles where runner is not blocked
    df0d = pbp[(pbp.EVENT_CD == e['Double']) & (pbp.RUN1_DEST_ID != 2) & \
               (pbp.RUN2_DEST_ID != 2) & (pbp.RUN3_DEST_ID != 2)]
    
    
    # Single where the hitter gets out and is not blocked
    d['0s_out'] = len(df0s[df0s.BAT_DEST_ID == 0])
    # Single where a hitter is safe and is not blocked
    d['0s_stay'] = len(df0s[df0s.BAT_DEST_ID == 1])
    
    # Normalize values
    batter_single = d['0s_out'] + d['0s_stay']
    d['0s_out'] = d['0s_out'] / batter_single
    d['0s_stay'] = d['0s_stay'] / batter_single
    
    # Double where the hitter is out and is not blocked
    d['0d_out'] = len(df0d[df0d.BAT_DEST_ID == 0])
    # Double where the hitter is safe and is not blocked
    d['0d_stay'] = len(df0d[df0d.BAT_DEST_ID == 2])
    
    # Normalize values
    batter_double = d['0d_out'] + d['0d_stay']
    d['0d_out'] = d['0d_out'] / batter_double
    d['0d_stay'] = d['0d_stay'] / batter_double
    
    # Type (3) Frequency of tagging
    # Assume that runners do not tag from first base
    
    # Get fly balls with runner on second that isn't blocked
    df2f = pbp[(~pbp.BASE2_RUN_ID.isna()) & (pbp.BASE3_RUN_ID.isna()) & \
               (pbp.BATTEDBALL_CD == 'F') & (pbp.EVENT_CD == e['Generic out'])]
    
    # Get fly balls with runner on third
    df3f = pbp[(~pbp.BASE3_RUN_ID.isna()) & (pbp.BATTEDBALL_CD == 'F') & \
               (pbp.EVENT_CD == e['Generic out'])]
    
    d['2f_advance'] = len(df2f[df2f.RUN2_DEST_ID == 3])
    d['2f_stay'] = len(df2f[df2f.RUN2_DEST_ID == 2])
    d['2f_out'] = len(df2f[(df2f.RUN2_DEST_ID == 0) & \
                         (~df2f.RUN2_PLAY_TX.isna())])
    
    # Normalize tagging from second to get frequencies
    second_tag = d['2f_advance'] + d['2f_stay'] + d['2f_out']
    d['2f_advance'] = d['2f_advance'] / second_tag
    d['2f_stay'] = d['2f_stay'] / second_tag
    d['2f_out'] = d['2f_out'] / second_tag
    
    d['3f_advance'] = len(df3f[df3f.RUN3_DEST_ID >= 4])
    d['3f_stay'] = len(df3f[df3f.RUN3_DEST_ID == 3])
    d['3f_out'] = len(df3f[(df3f.RUN3_DEST_ID == 0) & \
                             (~df3f.RUN3_PLAY_TX.isna())])
    
    # Normalize tagging from third to get frequencies
    third_tag = d['3f_advance'] + d['3f_stay'] + d['3f_out']
    d['3f_advance'] = d['3f_advance'] / third_tag
    d['3f_stay'] = d['3f_stay'] / third_tag
    d['3f_out'] = d['3f_out'] / third_tag
    
    return d

def ubr_score(pbp, pid, freq, run):
    ''' 
    Calculate a player's UBR given play-by-play data and an UBR frequency
    dictionary
    
    Arguments:
        pbp: retrosheet play by play data to calculate the given player's UBR
        pid: player id
        freq: the frequency of advancement on UBR related plays
        run: run matrix (dataframe)
    
    Output:
        ubr: value of a player's UBR given play by play data
    '''
    e = retrosheet_event_dict()
    
    # Type 1 UBR
    
    # Runner on first single not blocked
    df1s = pbp[(pbp.BASE1_RUN_ID == pid) & (pbp.EVENT_CD == e['Single']) & \
               (pbp.RUN3_DEST_ID != 3) & (pbp.RUN2_DEST_ID != 3)]
    
    # Calculate the advance, stay, out states unless inning ends
    # Add out if actual state was not out
    df1s['adv'] = df1s.new_state.apply(lambda x: '101' + x[3:])
    df1s['stay'] = df1s.new_state.apply(lambda x: '110' + x[3:])
    df1s['out'] = df1s.new_state.apply(lambda x: '100 ' + str(int(x[4]) + 1))
    
    # Subtract an out from hypotheticals if actual out occurred
    for ix in df1s[df1s.EVENT_OUTS_CT > 0].index:
        num_outs = str(int(df1s.at[ix, 'out'][4]) - 1)
        df1s.at[ix, 'adv'] = df1s.at[ix, 'adv'][:4] + num_outs
        df1s.at[ix, 'stay'] = df1s.at[ix, 'stay'][:4] + num_outs
        df1s.at[ix, 'out'] = df1s.at[ix, 'out'][:4] + num_outs
    
    # Reset index and get the original run values
    df1s = df1s.reset_index(drop=True)         
    orig_val = run.loc[df1s.state,].reset_index().loc[:, 'RUNS_ROI']
    
    # Calculate the value generated by each hypothetical state
    df1s_adv = run.loc[df1s.adv,].reset_index().loc[:, 'RUNS_ROI'] \
                - orig_val + df1s.runs_scored
    df1s_stay = run.loc[df1s.stay,].reset_index().loc[:, 'RUNS_ROI'] \
                - orig_val + df1s.runs_scored
    df1s_out = run.loc[df1s.out,].reset_index().loc[:, 'RUNS_ROI'] \
                - orig_val + df1s.runs_scored
                
    # Calculate the expected run values given frequency
    df1s_exp_runs = freq['1s_advance'] * df1s_adv + \
                    freq['1s_stay'] * df1s_stay + freq['1s_out'] * df1s_out
    
    # Calculate the UBR by the difference in runs expectation
    ubr = (df1s.runs_value - df1s_exp_runs).sum()
    
    # Runner on first double not blocked
    df1d = pbp[(pbp.BASE1_RUN_ID == pid) & (pbp.EVENT_CD == e['Double'])]
    
    # Calculate the advance, stay, out states unless inning ends
    df1d['adv'] = df1d.new_state.apply(lambda x: '010' + x[3:])
    df1d['stay'] = df1d.new_state.apply(lambda x: '011' + x[3:])
    df1d['out'] = df1d.new_state.apply(lambda x: '010 ' + str(int(x[4]) + 1))
    
    # Subtract an out from hypotheticals if actual out occurred
    for ix in df1d[df1d.EVENT_OUTS_CT > 0].index:
        num_outs = str(int(df1d.at[ix, 'out'][4]) - 1)
        df1d.at[ix, 'adv'] = df1d.at[ix, 'adv'][:4] + num_outs
        df1d.at[ix, 'stay'] = df1d.at[ix, 'stay'][:4] + num_outs
        df1d.at[ix, 'out'] = df1d.at[ix, 'out'][:4] + num_outs
    
    # Reset index and get the original run values
    df1d = df1d.reset_index(drop=True)         
    orig_val = run.loc[df1d.state,].reset_index().loc[:, 'RUNS_ROI']
    
    # Calculate the value generated by each hypothetical state
    df1d_adv = run.loc[df1d.adv,].reset_index().loc[:, 'RUNS_ROI'] \
                - orig_val + df1d.runs_scored
    df1d_stay = run.loc[df1d.stay,].reset_index().loc[:, 'RUNS_ROI'] \
                - orig_val + df1d.runs_scored
    df1d_out = run.loc[df1d.out,].reset_index().loc[:, 'RUNS_ROI'] \
                - orig_val + df1d.runs_scored
                
    # Calculate the expected run values given frequency
    df1d_exp_runs = freq['1d_advance'] * df1d_adv + \
                    freq['1d_stay'] * df1d_stay + freq['1d_out'] * df1d_out
    
    # Calculate the UBR by the difference in runs expectation
    ubr += (df1d.runs_value - df1d_exp_runs).sum()
    
    # Runner on second single
    df2s = pbp[(pbp.BASE2_RUN_ID == pid) & (pbp.EVENT_CD == e['Single'])]
    
     # Calculate the advance, stay, out states unless inning ends
    df2s['adv'] = df2s.new_state.apply(lambda x: x[:2] + '0' + x[3:])
    df2s['stay'] = df2s.new_state.apply(lambda x: x[:2] + '1' + x[3:])
    df2s['out'] = df2s.new_state.apply(lambda x: x[:2] + '0 ' + \
                    str(int(x[4]) + 1))
    
    # Subtract an out from hypotheticals if actual out occurred
    for ix in df2s[df2s.EVENT_OUTS_CT > 0].index:
        num_outs = str(int(df2s.at[ix, 'out'][4]) - 1)
        df2s.at[ix, 'adv'] = df2s.at[ix, 'adv'][:4] + num_outs
        df2s.at[ix, 'stay'] = df2s.at[ix, 'stay'][:4] + num_outs
        df2s.at[ix, 'out'] = df2s.at[ix, 'out'][:4] + num_outs
    
    # Reset index and get the original run values
    df2s = df2s.reset_index(drop=True)         
    orig_val = run.loc[df2s.state,].reset_index().loc[:, 'RUNS_ROI']
    
    # Calculate the value generated by each hypothetical state
    df2s_adv = run.loc[df2s.adv,].reset_index().loc[:, 'RUNS_ROI'] \
                - orig_val + df2s.runs_scored
    df2s_stay = run.loc[df2s.stay,].reset_index().loc[:, 'RUNS_ROI'] \
                - orig_val + df2s.runs_scored
    df2s_out = run.loc[df2s.out,].reset_index().loc[:, 'RUNS_ROI'] \
                - orig_val + df2s.runs_scored
                
    # Calculate the expected run values given frequency
    df2s_exp_runs = freq['2s_advance'] * df2s_adv + \
                    freq['2s_stay'] * df2s_stay + freq['2s_out'] * df2s_out
    
    # Calculate the UBR by the difference in runs expectation
    ubr += (df2s.runs_value - df2s_exp_runs).sum()
    
    # Type 2 UBR

    # Batter hits single
    df0s = pbp[(pbp.EVENT_CD == e['Single']) & (pbp.RUN1_DEST_ID != 2) & \
               (pbp.RESP_BAT_ID == pid)]

    df0s['out'] = df0s.new_state.apply(lambda x: '00' + x[2:4] + \
                    str(int(x[4]) + 1))
    df0s['stay'] = df0s.new_state.apply(lambda x: '10' + x[2:])
    
    # Subtract an out from hypotheticals if actual out occurred
    for ix in df0s[~df0s.BAT_PLAY_TX.isna()].index:
        num_outs = str(int(df0s.at[ix, 'out'][4]) - 1)
        df0s.at[ix, 'stay'] = df0s.at[ix, 'stay'][:4] + num_outs
        df0s.at[ix, 'out'] = df0s.at[ix, 'out'][:4] + num_outs
    
    # Reset index and get the original run values
    df0s = df0s.reset_index(drop=True)         
    orig_val = run.loc[df0s.state,].reset_index().loc[:, 'RUNS_ROI']
    
    # Calculate the value generated by each hypothetical state
    df0s_stay = run.loc[df0s.stay,].reset_index().loc[:, 'RUNS_ROI'] \
                - orig_val + df0s.runs_scored
    df0s_out = run.loc[df0s.out,].reset_index().loc[:, 'RUNS_ROI'] \
                - orig_val + df0s.runs_scored
                
    # Calculate the expected run values given frequency
    df0s_exp_runs = freq['0s_stay'] * df0s_stay + freq['0s_out'] * df0s_out
    
    # Calculate the UBR by the difference in runs expectation
    ubr += (df0s.runs_value - df0s_exp_runs).sum()

    # Batter hits double
    df0d = pbp[(pbp.EVENT_CD == e['Double']) & (pbp.RUN1_DEST_ID != 2) & \
                   (pbp.RUN2_DEST_ID != 2) & (pbp.RESP_BAT_ID == pid)]
    
    df0d['out'] = df0d.new_state.apply(lambda x: '000 ' + str(int(x[4]) + 1))
    df0d['stay'] = df0d.new_state.apply(lambda x: '010 ' + x[4])
    
    # Subtract an out from hypotheticals if actual out occurred
    for ix in df0d[~df0d.BAT_PLAY_TX.isna()].index:
        num_outs = str(int(df0d.at[ix, 'out'][4]) - 1)
        df0d.at[ix, 'stay'] = df0d.at[ix, 'stay'][:4] + num_outs
        df0d.at[ix, 'out'] = df0d.at[ix, 'out'][:4] + num_outs
    
    # Reset index and get the original run values
    df0d = df0d.reset_index(drop=True)         
    orig_val = run.loc[df0d.state,].reset_index().loc[:, 'RUNS_ROI']
    
    # Calculate the value generated by each hypothetical state
    df0d_stay = run.loc[df0d.stay,].reset_index().loc[:, 'RUNS_ROI'] \
                - orig_val + df0d.runs_scored
    df0d_out = run.loc[df0d.out,].reset_index().loc[:, 'RUNS_ROI'] \
                - orig_val + df0d.runs_scored
                
    # Calculate the expected run values given frequency
    df0d_exp_runs = freq['0d_stay'] * df0d_stay + freq['0d_out'] * df0d_out
    
    # Calculate the UBR by the difference in runs expectation
    ubr += (df0d.runs_value - df0d_exp_runs).sum()
    
    # Type 3 UBR
    
    # Tagging from second base
    df2f = pbp[(pbp.BASE2_RUN_ID == pid) & (pbp.BASE3_RUN_ID.isna()) & 
               (pbp.BATTEDBALL_CD == 'F')]
    
    # Calculate the advance, stay, out states unless inning ends
    # Add out if actual state was not out
    df2f['adv'] = df2f.new_state.apply(lambda x: x[:2] + '1' + x[3:])
    df2f['stay'] = df2f.new_state.apply(lambda x: x[:1] + '10' + x[3:])
    df2f['out'] = df2f.new_state.apply(lambda x: x[:2] + '0 ' + \
                    str(int(x[4]) + 1))
    
    # Subtract an out from hypotheticals if actual out occurred
    for ix in df2f[df2f.EVENT_OUTS_CT > 1].index:
        num_outs = str(int(df2f.at[ix, 'out'][4]) - 1)
        df2f.at[ix, 'adv'] = df2f.at[ix, 'adv'][:4] + num_outs
        df2f.at[ix, 'stay'] = df2f.at[ix, 'stay'][:4] + num_outs
        df2f.at[ix, 'out'] = df2f.at[ix, 'out'][:4] + num_outs
    
    # Reset index and get the original run values
    df2f = df2f.reset_index(drop=True)         
    orig_val = run.loc[df2f.state,].reset_index().loc[:, 'RUNS_ROI']
    
    # Calculate the value generated by each hypothetical state
    df2f_adv = run.loc[df2f.adv,].reset_index().loc[:, 'RUNS_ROI'] \
                - orig_val + df2f.runs_scored
    df2f_stay = run.loc[df2f.stay,].reset_index().loc[:, 'RUNS_ROI'] \
                - orig_val + df2f.runs_scored
    df2f_out = run.loc[df2f.out,].reset_index().loc[:, 'RUNS_ROI'] \
                - orig_val + df2f.runs_scored
                
    # Calculate the expected run values given frequency
    df2f_exp_runs = freq['2f_advance'] * df2f_adv + \
                    freq['2f_stay'] * df2f_stay + freq['2f_out'] * df2f_out
    
    # Calculate the UBR by the difference in runs expectation
    ubr += (df2f.runs_value - df2f_exp_runs).sum()

    # Tagging from third base
    df3f = pbp[(pbp.BASE3_RUN_ID == pid) & (pbp.BATTEDBALL_CD =='F')]
    
    # Calculate the advance, stay, out states unless inning ends
    df3f['adv'] = df3f.new_state.apply(lambda x: x[:2] + '0' + x[3:])
    df3f['stay'] = df3f.new_state.apply(lambda x: x[:2] + '1' + x[3:])
    df3f['out'] = df3f.new_state.apply(lambda x: x[:2] + '0 ' + \
                    str(int(x[4]) + 1))
    
    # Subtract an out from hypotheticals if actual out occurred
    for ix in df3f[df3f.EVENT_OUTS_CT > 1].index:
        num_outs = str(int(df3f.at[ix, 'out'][4]) - 1)
        df3f.at[ix, 'adv'] = df3f.at[ix, 'adv'][:4] + num_outs
        df3f.at[ix, 'stay'] = df3f.at[ix, 'stay'][:4] + num_outs
        df3f.at[ix, 'out'] = df3f.at[ix, 'out'][:4] + num_outs
    
    # Reset index and get the original run values
    df3f = df3f.reset_index(drop=True)         
    orig_val = run.loc[df3f.state,].reset_index().loc[:, 'RUNS_ROI']
    
    # Calculate the value generated by each hypothetical state
    df3f_adv = run.loc[df3f.adv,].reset_index().loc[:, 'RUNS_ROI'] \
                - orig_val + df3f.runs_scored
    df3f_stay = run.loc[df3f.stay,].reset_index().loc[:, 'RUNS_ROI'] \
                - orig_val + df3f.runs_scored
    df3f_out = run.loc[df3f.out,].reset_index().loc[:, 'RUNS_ROI'] \
                - orig_val + df3f.runs_scored
                
    # Calculate the expected run values given frequency
    df3f_exp_runs = freq['3f_advance'] * df3f_adv + \
                    freq['3f_stay'] * df3f_stay + freq['3f_out'] * df3f_out
    
    # Calculate the UBR by the difference in runs expectation
    ubr += (df3f.runs_value - df3f_exp_runs).sum()
    
    return ubr

def wSB_constants(pbp):
    ''' Calculate constants lgwSB, runSB, runCS for a set of play by play data
    
    Arguments:
        pbp: retrosheet play-by-play data
        
    Output: dictionary containing values for the three following constants
        lgwSB is the league's weigthed stolen base calculated by 
            (SB * runSB + CS * runCS) / (1B + BB + HBP - IBB)
        runSB is the average run value of a stolen base
        runCS is the average run value of a caught stealing 
    '''
    
    e = retrosheet_event_dict()
    d = {}
    
    # Calculate average run values of caught stealing and stolen base
    df_SB = pbp[pbp.EVENT_CD == e['Stolen base']]
    d['runSB'] = df_SB.runs_value.mean()
    df_CS = pbp[pbp.EVENT_CD == e['Caught stealing']]
    d['runCS'] = df_CS.runs_value.mean()
    
    # Calculate constants for lgwSB formula
    SB = len(df_SB)
    CS = len(df_CS)
    Single = len(pbp[pbp.EVENT_CD == e['Single']])
    BB = len(pbp[pbp.EVENT_CD == e['Walk']])
    HBP = len(pbp[pbp.EVENT_CD == e['Hit by pitch']])
    IBB = len(pbp[pbp.EVENT_CD == e['Intentional walk']])
    
    d['lgwSB'] = (SB*d['runSB'] + CS*d['runCS']) / (Single + BB + HBP - IBB)
    
    return d 

def wSB_score(pbp, pid, wSB_const):
    ''' Calculate a player's wSB
    
    Arguments:
        pbp: retrosheet play by play data
        pid: player ID for player to calculate wSB
        wSB_const: constants needed to calculate wSB (lgwSB, runSB, runCS)
    
    Output: wSB value for the player
    '''
    e = retrosheet_event_dict()
    
    # Get play by play data where the player is a non blocked runner
    # Assume that runner does not steal home
    runner = pbp[((pbp.BASE1_RUN_ID == pid) & (pbp.BASE2_RUN_ID.isna())) \
                 | ((pbp.BASE2_RUN_ID == pid) & (pbp.BASE3_RUN_ID.isna()))]
    
    # Get the number of stolen bases and caught stealing by player when he
    # is not blocked. We don't count trailing steals
    SB = len(runner[runner.EVENT_CD == e['Stolen base']])
    CS = len(runner[runner.EVENT_CD == e['Caught stealing']])
    
    # Get play by play data where the batter is the responsible batter
    bat = pbp[(pbp.RESP_BAT_ID == pid) & (pbp.BAT_EVENT_FL == 'T')]
    
    # Get number of batting events for events used in wSB calculation
    Single = len(bat[bat.EVENT_CD == e['Single']])
    BB = len(bat[bat.EVENT_CD == e['Walk']])
    HBP = len(bat[bat.EVENT_CD == e['Hit by pitch']])
    IBB = len(bat[bat.EVENT_CD == e['Intentional walk']])
    
    # Extract constants and calculate wSB
    runSB = wSB_const['runSB']
    runCS = wSB_const['runCS']
    lgwSB = wSB_const['lgwSB']
    return (SB * runSB + CS * runCS) - lgwSB * (Single + BB + HBP - IBB)
#%%
def wOBA_constants(pbp):
    ''' Calculate constants for wOBA which is the average runs value for 
    unintentional walks, hit by pitches, first base, second base, third base,
    and home runs, league_wOBA, wOBA_scale
    
    Arguments:
        pbp: retrosheet play-by-play data
        
    Output: dictionary containing run values for the events occured above
    '''
    e = retrosheet_event_dict()
    d = {}
    
    # Get dataframe of batting events
    bat = pbp[pbp.BAT_EVENT_FL == 'T']
    
    # Calculate linear_weight of batting outs to scale constants
    out_weight = pbp[(pbp.BAT_EVENT_FL == 'T') & \
                    (pbp.EVENT_OUTS_CT > 0)].runs_value.mean()
    
    # Calculate average run values for each event
    d['BB'] = pbp[pbp.EVENT_CD == e['Walk']].runs_value.mean()
    d['HBP'] = pbp[pbp.EVENT_CD == e['Hit by pitch']].runs_value.mean()
    d['1B'] = pbp[pbp.EVENT_CD == e['Single']].runs_value.mean()
    d['2B'] = pbp[pbp.EVENT_CD == e['Double']].runs_value.mean()
    d['3B'] = pbp[pbp.EVENT_CD == e['Triple']].runs_value.mean()
    d['HR'] = pbp[pbp.EVENT_CD == e['Home run']].runs_value.mean()
    
    # Calculate the wOBA scale. Match league wOBA to league OBP with IBB 
    # removed. w0BA scale = league OBP - IBB / league wOBA
    
    # Calculate number of events that ococurred for the league
    gen_outs = (bat.EVENT_CD == e['Generic out']).sum()
    strikeouts = (bat.EVENT_CD == e['Strikeout']).sum()
    errors = (bat.EVENT_CD == e['Error']).sum()
    FC = (bat.EVENT_CD == e['Fielder choice']).sum()
    BB = (bat.EVENT_CD == e['Walk']).sum()
    HBP = (bat.EVENT_CD == e['Hit by pitch']).sum()
    single = (bat.EVENT_CD == e['Single']).sum()
    double = (bat.EVENT_CD == e['Double']).sum()
    triple = (bat.EVENT_CD == e['Triple']).sum()
    homerun = (bat.EVENT_CD == e['Home run']).sum()
    hits = single + double + triple + homerun
    IBB = (bat.EVENT_CD == e['Intentional walk']).sum()
    SF = (bat.SF_FL == 'T').sum()
    AB = hits + gen_outs + strikeouts + FC + errors
    PA = len(bat)
    
    # Calculate League OBP not including intentional walks
    league_OBP = (hits + BB + HBP) / PA
    
    # Scale by subtracting average weight of an out
    for key, _ in d.items():
        d[key] -= out_weight
    
    # Calculate League wOBA
    wOBA_top = d['BB']*BB + d['HBP']*HBP + d['1B']*single + \
                    d['2B']*double + d['3B']*triple + d['HR']*homerun
    wOBA_bot = AB + BB - IBB + SF + HBP
    league_wOBA = wOBA_top / wOBA_bot
    
    # Calculate scale OBP (no IBB) / wOBA
    d['wOBA_scale'] = league_OBP / league_wOBA
    
    # Scale by multiplying by wOBA scale
    for key, _ in d.items():
        d[key] *= d['wOBA_scale']
        
    # Add updated league wOBA
    wOBA_top = d['BB']*BB + d['HBP']*HBP + d['1B']*single + \
                    d['2B']*double + d['3B']*triple + d['HR']*homerun
    d['league_wOBA'] = wOBA_top / wOBA_bot

    return d

#%%

def wOBA_score(pbp, pid, wOBA_const):
    ''' Calculate a player's wOBA
    
    Arguments:
        pbp: retrosheet play by play data
        pid: player ID for player to calculate wSB
        wOBOA_const: constants needed to calculate wOBA. there are weights
            for uBB, HBP, 1B, 2B, 3B, HR
    
    Output: wOBA value for the player
    '''
    e = retrosheet_event_dict()
    bat = pbp[(pbp.RESP_BAT_ID == pid) & (pbp.BAT_EVENT_FL == 'T')]
    
    # Calculate number of events that ococurred for the league
    gen_outs = (bat.EVENT_CD == e['Generic out']).sum()
    strikeouts = (bat.EVENT_CD == e['Strikeout']).sum()
    errors = (bat.EVENT_CD == e['Error']).sum()
    FC = (bat.EVENT_CD == e['Fielder choice']).sum()
    BB = (bat.EVENT_CD == e['Walk']).sum()
    HBP = (bat.EVENT_CD == e['Hit by pitch']).sum()
    single = (bat.EVENT_CD == e['Single']).sum()
    double = (bat.EVENT_CD == e['Double']).sum()
    triple = (bat.EVENT_CD == e['Triple']).sum()
    homerun = (bat.EVENT_CD == e['Home run']).sum()
    hits = single + double + triple + homerun
    IBB = (bat.EVENT_CD == e['Intentional walk']).sum()
    SF = (bat.SF_FL == 'T').sum()
    AB = hits + gen_outs + strikeouts + FC + errors
    
    # Calculate top and bottom wOBA
    wOBA_top = wOBA_const['BB'] * BB + wOBA_const['HBP'] * HBP + \
                wOBA_const['1B'] * single + wOBA_const['2B'] * double + \
                wOBA_const['3B'] * triple + wOBA_const['HR'] * homerun
    wOBA_bot = AB + BB - IBB + SF + HBP
    
    return wOBA_top / wOBA_bot

def get_park_factors(pbp):
    ''' Get park factors for all teams in play by play data
    
    Park factor will be cauclated as:
        [(home_RS + home_RA) / home_G] / [(road_RS + road_RA) / road_G]
    
    Argument: retrosheet play by play
    
    Output: dictionary containing park factor for each team
    '''
    d = {}
    
    # Get home team ID and away team id
    pbp['home'] = pbp.GAME_ID.str.slice(0, 3)
    pbp['away'] = pbp.AWAY_TEAM_ID
    
    pbp = pbp.loc[:, ['GAME_ID', 'home', 'away', 'HOME_SCORE_CT', 
                      'AWAY_SCORE_CT']]
    # Get teams that had both a home and away game
    teams = set(pbp.home.append(pbp.away))
    
    # Get park factors for each team
    for team in teams:
        # Create home and away dataframes
        df_home = pbp[pbp.home == team]
        df_away = pbp[pbp.away == team]
        
        # Get Runs Scored, allowed, and Games at Home
        home_RS = df_home.groupby(['GAME_ID']).max().loc[:, 
                                 'HOME_SCORE_CT'].sum()
        home_RA = df_home.groupby(['GAME_ID']).max().loc[:,
                                 'AWAY_SCORE_CT'].sum()
        home_G = len(df_home['GAME_ID'].unique())
        
        # Get Runs Scored, Allowed, and Games Away
        away_RS = df_away.groupby(['GAME_ID']).max().loc[:,
                                 'AWAY_SCORE_CT'].sum()
        away_RA = df_away.groupby(['GAME_ID']).max().loc[:,
                                 'HOME_SCORE_CT'].sum() 
        away_G = len(df_away['GAME_ID'].unique())
        
        # Get park factor
        home_pf = (home_RS + home_RA) / home_G
        away_pf = (away_RS + away_RA) / away_G
        d[team] = home_pf / away_pf
    return d

def advanced_batting(pbp, df, runs_pbp):
    ''' Add all advanced batting statistics to a dataframe. Standard stats
    must be calculated before advanced stats
    
    Advanced Stats: BB%, K%, BB/K, OBP, SLG, OPS, ISO, SPD, BABIP, UBR, wGDP,
                    wSB, wRC, wRAA, wOBA
    
    Arguments:
        pbp: play by play data for a given period to calculate statistics for
        df: dataframe with players to calculate standard statistics for
        runs_pbp: play by play data to calculate run matrix
        
    Output:
        dataframe with advanced stats appended
    '''
    
    # Add Runs Value to play by play data
    runs_matrix = create_runs_matrix(runs_pbp)
    pbp = add_runs_value(pbp, runs_matrix)
    
    # Calculate the frequencies for ultimate base running
    ubr_freq = ubr_run_frequency(runs_pbp)
    
    # Obtain double play run values as dictionary
    dp_avg = double_play_run_values(runs_pbp)
    
    # Get constants for weighted stolen base
    wSB_const = wSB_constants(runs_pbp)
    
    # Get constants for weighted OBA
    wOBA_const = wOBA_constants(runs_pbp)
    
    # Calculate total runs and total PA
    total_PA = (pbp.BAT_EVENT_FL == 'T').sum()
    pbp_runs = pbp.loc[:, ['GAME_ID', 'AWAY_SCORE_CT', 'HOME_SCORE_CT']]
    home_runs = pbp_runs.groupby(['GAME_ID']).max().loc[:, 
                                'HOME_SCORE_CT'].sum()
    away_runs = pbp_runs.groupby(['GAME_ID']).max().loc[:,
                                'AWAY_SCORE_CT'].sum()
    total_runs = home_runs + away_runs
    R_per_PA = total_runs / total_PA
    
    # Calculate park factors
    pf = get_park_factors(runs_pbp)
    
    # iterate through every player in the dataframe
    for ix, row in df.iterrows():
        
        # Get player id for the current row
        pid = row['ID']

        # BB%
        df.at[ix, 'BB%'] = round(100 * df.at[ix, 'BB'] / df.at[ix, 'PA'], 2)
        
        # K%
        df.at[ix, 'K%'] = round(100 * df.at[ix, 'SO'] / df.at[ix, 'PA'], 2)
        
        # BB/K
        df.at[ix, 'BB/K'] = round(df.at[ix, 'BB'] / df.at[ix, 'SO'], 2)
        
        # OBP
        OBP_top = df.at[ix, 'H'] + df.at[ix, 'BB'] + df.at[ix, 'IBB'] + \
                    df.at[ix, 'HBP']
        df.at[ix, 'OBP'] = round(OBP_top / df.at[ix, 'PA'], 3)
        
        # SLG
        slg_1B = df.at[ix, '1B']
        slg_2B = df.at[ix, '2B']
        slg_3B = df.at[ix, '3B']
        slg_HR = df.at[ix, 'HR']
        slg_top = slg_1B + slg_2B + slg_3B + slg_HR
        df.at[ix, 'SLG'] = round(slg_top / df.at[ix, 'AB'], 3)
        
        # OPS
        df.at[ix, 'OPS'] = round(df.at[ix, 'OBP'] + df.at[ix, 'SLG'], 3)
        
        # ISO
        df.at[ix, 'ISO'] = df.at[ix, 'SLG'] - df.at[ix, 'AVG']
        
        # SPD. 4 component version. Average of stolen base percentage,
        # frequency of stolen base attempts, percentage of triples, and
        # runs scored percentage
        
        # https://en.wikipedia.org/wiki/Speed_Score
        
        # Factor 1: Stolen Base Percentage
        # Set variables for necessary standard stats
        SB = df.at[ix, 'SB']
        CS = df.at[ix, 'CS']
        Singles = df.at[ix, '1B']
        BB = df.at[ix, 'BB']
        HBP = df.at[ix, 'HBP']
        HR = df.at[ix, 'HR']
        AB = df.at[ix, 'AB']
        Triples = df.at[ix, '3B']
        R = df.at[ix, 'R']
        SF = df.at[ix, 'SF']
        K = df.at[ix, 'SO']
        H = df.at[ix, 'H']
        
        SPD_F1 = 20 * ((SB + 3) / (SB + CS + 7) - 0.4)
        SPD_F2 = ((SB + CS) / (Singles + BB + HBP)) ** (0.5) / 0.07
        SPD_F3 = 625 * Triples / (AB - HR - K)
        SPD_F4 = 25 * ((R - HR) / (H + BB + HBP - HR) - 0.1)
        
        df.at[ix, 'Spd'] = round((SPD_F1 + SPD_F2 + SPD_F3 + SPD_F4) / 4, 1)
        
        # BABIP
        df.at[ix, 'BABIP'] = round((H - HR) / (AB - HR - K + SF), 3)
        
        # UBR
            # This statistic will be modified. We will only analyze 
            # success rate tagging and advancing extra bases on hits
            # https://www.fangraphs.com/library/offense/ubr/            
        df.at[ix, 'UBR'] = ubr_score(pbp, pid, ubr_freq, runs_matrix)
                
        # wGDP
        df.at[ix, 'wGDP'] = wGDP_score(pbp, pid, dp_avg)

        # wSB
        df.at[ix, 'wSB'] = wSB_score(pbp, pid, wSB_const)
        
        # wOBA
        df.at[ix, 'wOBA'] = wOBA_score(pbp, pid, wOBA_const)
        
        # wRAA
        df.at[ix, 'wRAA'] = (df.at[ix, 'wOBA'] - wOBA_const['league_wOBA']) \
                             / wOBA_const['wOBA_scale'] * df.at[ix, 'PA']
        
        # wRC
        df.at[ix, 'wRC'] = df.at[ix, 'wRAA'] + df.at[ix, 'PA'] * R_per_PA
        
        # BsR (Base Running Runs)
        df.at[ix, 'BsR'] = df.at[ix, 'UBR'] + df.at[ix, 'wGDP'] + \
                            df.at[ix, 'wSB']
        
    # wRC+ (Note we will not weight by NL/AL but simply all the data)
    wRC_avg = df['wRC'].mean()
    
    # Loop back through to calculate wRC+ since it is based on average of wRC
    for ix, _ in df.iterrows():
        pf_team = pf[df.at[ix, 'Team']]
        
        # wRC+
        # Account for park factors
        df.at[ix, 'wRC+'] = df.at[ix, 'wRC'] + (1 - pf_team) * R_per_PA 
        # scale
        df.at[ix, 'wRC+'] = df.at[ix, 'wRC+'] / wRC_avg * 100
        
        # Batting Runs (Don't take into account AL/NL)
        df.at[ix, 'Batting Runs'] = df.at[ix, 'wRAA'] + (1-pf_team) * R_per_PA
        
        # ORAA - Offensive Runs Above Average
        df.at[ix, 'ORAA'] = df.at[ix, 'Batting Runs'] + df.at[ix, 'BsR']
    return df

def batted_ball(pbp, df, runs_pbp):
    ''' Add some batted ball batting statistics to a dataframe
    
    Note: We don't have quality enough location data in retrosheet to have
    pull, cent, oppo. Also don't know if hits stay in the infield. Finally,
    don't know contact type
        
    Actual Batted Ball Stats: GB/FB, LD%, GB%, FB%, IFFB%, HR/FB, IFH (infield
    hits), IFH%, BUH (bunt hits), BUH%, Pull%, Cent%, Oppo%, Soft%, Med%, Hard%
        
    Batted Ball Stats Calculated: GB/FB, LD%, GB%, FB%, HR/ FB, BUH, BUH%, GB,
    FB, LD, IFFB, BU (bunts), 
    
    Arguments:
        pbp: play by play data for a given period to calculate statistics for
        df: dataframe with players to calculate standard statistics for
        runs_pbp: play by play data to calculate run matrix
        
    Output:
        dataframe with advanced stats appended
    '''
    
    e = retrosheet_event_dict()
    
    # Loop through every player 
    for ix, row in df.iterrows():
        
        # Get batting events for a specific player
        bat = pbp[(pbp.RESP_BAT_ID == row['ID']) & (pbp.BAT_EVENT_FL == 'T')]
        
        # Get frequency of events. ground ball, line drive, flyball, pop-ups
        gb = (bat.BATTEDBALL_CD == 'G').sum()
        ld = (bat.BATTEDBALL_CD == 'L').sum()
        fb = (bat.BATTEDBALL_CD == 'F').sum()
        iffb = (bat.BATTEDBALL_CD == 'P').sum()
        
        # fly balls include infield fly balls
        fb += iffb
        
        # Get the number of balls in play, home runs, pop-ups, bunts, bunt hits
        bip = gb + ld + fb
        
        bunt_hits = ((bat.EVENT_CD == e['Single']) & \
                            (bat.BUNT_FL == 'T')).sum()
        bunts = (bat.BUNT_FL == 'T').sum()
        hr = (bat.EVENT_CD == e['Home run']).sum()
        
        # Calculate ratios
        df.at[ix, 'GB/FB'] = round(gb / fb, 3)
        df.at[ix, 'LD%'] = round(100 * ld / bip, 2)
        df.at[ix, 'GB%'] = round(100 * gb / bip, 2)
        df.at[ix, 'FB%'] = round(100 * fb / bip, 2)
        df.at[ix, 'IFFB%'] = round(100 * iffb / bip, 2)
        df.at[ix, 'HR/FB'] = round(hr / fb, 3)
        df.at[ix, 'BUH'] = bunt_hits
        df.at[ix, 'BUH%'] = round(100 * bunt_hits / (bunt_hits + bunts), 2)
        df.at[ix, 'GB'] = gb
        df.at[ix, 'FB'] = fb
        df.at[ix, 'LD'] = ld
        df.at[ix, 'IFFB'] = iffb
        df.at[ix, 'BU'] = bunts
        
    return df

#%%

def runs_per_win(pbp):
    ''' Get the runs per win for play by play data
    
    Argument: retrosheet play by play data
    
    Output: runs per win value
    '''
    
    # Create standings for play by play data
    stand = create_standings(pbp)
    
    # Get average runs per game which would be total runs / 2 / G
    stand['G'] = stand.W + stand.L
    runs_per_game = (stand.R.sum() + stand.RA.sum()) / (2 * stand.G.sum())
    
    # Calculate pythagorean coefficient for R^x / (R^x + RA^x)
    stand['log_win_ratio'] = np.log(stand.W.astype(float) / \
                                 stand.L.astype(float))
    stand['log_run_ratio'] = np.log(stand.R / stand.RA)
    
    # Calculate lnear regression through origin in order to calculate proper
    # exponent
    wins = np.array(stand.log_win_ratio)
    runs = np.array(stand.log_run_ratio)[:, np.newaxis]
    
    pythagorean_coefficient = np.linalg.lstsq(runs, wins)[0][0]

    # return Caola derived runs per win
    return 4 * runs_per_game / pythagorean_coefficient

#%%
def win_probability(pbp, df, runs_pbp, wp_pbp, run_type='differential',
                    wp_standings=None, pbp_standings=None):
    ''' Add win probability data to dataframe. There are different options
    in run_type and standings to choose which model to calculate win
    probability from
    
    Standings data frame contains a team and their winning percentage 
    for a given season. Standings has index 'XXXYYY' where XXX is the team ID 
    and YYYY is the four digit year as index and an attribute for winning 
    percentage named 'WPct'
    
    NOTE: pbp should be a subset of wp_pbp.
    
    Also remmeber that WPA is not predictive
    
    Arguments:
        pbp: play by play data for a given period to calculate statistics for
        df: dataframe with players to calculate standard statistics for
        runs_pbp: play by play data to calculate run matrix
        wp_pbp: play by play data to calculate win probability
        run_type: string that is either 'differential' or 'score. If it is
        'differential' our game state contains (Home Score - Away Score). If it
        is 'score' our game state contains Home Score + '_' + Away Score.
        standings: data frame containing WPct of teams being evaluated. If this
        is not None then team records will be taken into account.
            
            wp_standings are standings for teams in wp_pbp data
            pbp_standings are standings for teams in pbp data
        
    Output:
        dataframe with advanced stats appended
    '''
    # Add wins_value to pbp using wp_pbp data. Use 
    wp_pbp = add_home_won(wp_pbp)
    wp_pbp = add_game_state(wp_pbp, run_type, wp_standings)
    win_matrix = win_prob_matrix(wp_pbp)
    
    pbp = add_home_won(pbp)
    pbp = add_game_state(pbp, run_type, pbp_standings)
    pbp = add_win_prob_value(pbp, win_matrix)
    
    # Add run_value expectancy
    run_matrix = create_runs_matrix(runs_pbp)
    pbp = add_runs_value(pbp, run_matrix)
    
    RPW = runs_per_win(pbp)
    # Loop through every player 
    for ix, row in df.iterrows():
        
        # Get batting events for a specific player
        bat = pbp[(pbp.RESP_BAT_ID == row['ID']) & (pbp.BAT_EVENT_FL == 'T')]
        
        # WPA (Win Probability Added)
        df.at[ix, 'WPA'] = bat.win_value.sum()
        
        # -WPA (Negative Win Probaiblity Added)
        df.at[ix, '-WPA'] = bat[bat.win_value < 0].win_value.sum()
        
        # + WPA (Positive Win Probability Added)
        df.at[ix, '+WPA'] = bat[bat.win_value > 0].win_value.sum()
        
        # RE24 (Run Expectancy 24 Base Out State)
        df.at[ix, 'RE24'] = bat.runs_value.sum()
        
        # REW (Run Expectancy Wins)
        df.at[ix, 'REW'] = df.at[ix, 'RE24'] / RPW
        
    return df
#%%
# =============================================================================
# #%% testing
# roster = pd.read_csv('roster2018.csv')
# names = [['Albert', 'Pujols'], ['Mike', 'Trout'], ['David', 'Fletcher']]
# #names = [['Mike', 'Trout']]
# from initialize_players import initialize_list_to_df
# df1 = initialize_list_to_df(roster, names)
# pbp = pd.read_csv('all2018.csv', header=None)
# fields = pd.read_csv('fields.csv')
# pbp.columns = fields.loc[:, 'Header']
# 
# #%%
# 
# df = standard_batting(pbp, df1)
# #df = advanced_batting(pbp, df, pbp)
# df = batted_ball(pbp, df, pbp)
# 
# =============================================================================
#%% WPA testing
roster = pd.read_csv('roster2018.csv')
#names = [['Albert', 'Pujols'], ['Mike', 'Trout'], ['David', 'Fletcher']]
names = [['Mike', 'Trout']]
from initialize_players import initialize_list_to_df
df1 = initialize_list_to_df(roster, names)

pbp = pd.read_csv('all2018.csv', header=None)
pbp2017 = pd.read_csv('all2017.csv', header=None)
pbp2016 = pd.read_csv('all2016.csv', header=None)
pbp2015 = pd.read_csv('all2015.csv', header=None)
pbp2014 = pd.read_csv('all2014.csv', header=None)

wp_pbp = pbp.append(pbp2017)
wp_pbp = wp_pbp.append(pbp2016)
wp_pbp = wp_pbp.append(pbp2015)
wp_pbp = wp_pbp.append(pbp2014)


fields = pd.read_csv('fields.csv')
pbp.columns = fields.loc[:, 'Header']
wp_pbp.columns = fields.loc[:, 'Header']

df = standard_batting(pbp, df1)

stand_wp_pbp = create_standings(wp_pbp)
stand_pbp = create_standings(pbp)

#%%
df2 = win_probability(pbp, df, pbp, wp_pbp, run_type='differential',
                     wp_standings=stand_wp_pbp, pbp_standings=stand_pbp)


