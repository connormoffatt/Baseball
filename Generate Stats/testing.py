import pandas as pd
import numpy as np
from general import retrosheet_event_dict
import re
import random
#%% Initialize Players
# =============================================================================
# 
# #%%
# # Initialize testing list to list
# roster = pd.read_csv('roster2018.csv')
# names = [['Albert', 'Pujols'], ['Mike', 'Trout'], ['David', 'Fletcher']]
# 
# from initialize_players import initialize_list_to_list
# 
# player = initialize_list_to_list(roster, names)
# 
# 
# #%%
# # Initialize testing LIST TO DATAFRAME
# from initialize_players import initialize_list_to_df
# df1 = initialize_list_to_df(roster, names)
# 
# #%% Initialize testing DF to DF
# df_names = df1.drop(columns=['ID'])
# from initialize_players import initialize_df_to_df
# df2 = initialize_df_to_df(roster, df_names)
# 
# 
# =============================================================================
#%%
#%% testing
roster = pd.read_csv('roster2018.csv')
names = [['Albert', 'Pujols'], ['Mike', 'Trout'], ['David', 'Fletcher']]
#names = [['Mike', 'Trout']]
from initialize_players import initialize_list_to_df
df1 = initialize_list_to_df(roster, names)
pbp = pd.read_csv('all2018.csv', header=None)
fields = pd.read_csv('fields.csv')
pbp.columns = fields.loc[:, 'Header']
from batting import standard_batting
from batting import advanced_batting


df = standard_batting(pbp, df1)
df = advanced_batting(pbp, df, pbp)
#df = batted_ball(pbp, df, pbp)
#%%
# =============================================================================
# #%% WPA testing
# roster = pd.read_csv('roster2018.csv')
# #names = [['Albert', 'Pujols'], ['Mike', 'Trout'], ['David', 'Fletcher']]
# names = [['Mike', 'Trout']]
# from initialize_players import initialize_list_to_df
# df1 = initialize_list_to_df(roster, names)
# 
# pbp = pd.read_csv('all2018.csv', header=None)
# pbp2017 = pd.read_csv('all2017.csv', header=None)
# pbp2016 = pd.read_csv('all2016.csv', header=None)
# pbp2015 = pd.read_csv('all2015.csv', header=None)
# pbp2014 = pd.read_csv('all2014.csv', header=None)
# 
# wp_pbp = pbp.append(pbp2017)
# wp_pbp = wp_pbp.append(pbp2016)
# wp_pbp = wp_pbp.append(pbp2015)
# wp_pbp = wp_pbp.append(pbp2014)
# 
# 
# fields = pd.read_csv('fields.csv')
# pbp.columns = fields.loc[:, 'Header']
# wp_pbp.columns = fields.loc[:, 'Header']
# 
# df = standard_batting(pbp, df1)
# 
# stand_wp_pbp = create_standings(wp_pbp)
# stand_pbp = create_standings(pbp)
# 
# #%%
# df2 = win_probability(pbp, df, pbp, wp_pbp, run_type='differential',
#                      wp_standings=stand_wp_pbp, pbp_standings=stand_pbp)
# 
# 
# 
# 
# =============================================================================

#%% FIELDING TESTING

# =============================================================================
# pbp = pd.read_csv('all2018.csv', header=None)
# fields = pd.read_csv('fields.csv')
# pbp.columns = fields.loc[:, 'Header']
# pbp2 = pbp
# 
# =============================================================================
pbp = pd.read_csv('all2018.csv', header=None)
# =============================================================================
# pbp2017 = pd.read_csv('all2017.csv', header=None)
# pbp2016 = pd.read_csv('all2016.csv', header=None)
# pbp2015 = pd.read_csv('all2015.csv', header=None)
# pbp2014 = pd.read_csv('all2014.csv', header=None)
# 
# pbp = pbp.append(pbp2017)
# pbp = pbp.append(pbp2016)
# pbp = pbp.append(pbp2015)
# pbp = pbp.append(pbp2014)
# =============================================================================
#pbp = pbp.head(30)

fields = pd.read_csv('fields.csv')
pbp.columns = fields.loc[:, 'Header']


# =============================================================================
# #%%
# e = retrosheet_event_dict()
# ball_in_play = [e['Single'], e['Double'], e['Triple'], e['Generic out'],
#                 e['Error'], e['Fielder choice']]
# 
# # location will be a string ff
# # Get event text for all balls in play
# pbp['location'] = np.where(pbp.EVENT_CD.isin(ball_in_play), pbp.EVENT_TX, None)
# 
# # Single, Triple, and Error
# pbp['location'] = np.where((pbp.EVENT_CD == e['Single']) | \
#         (pbp.EVENT_CD == e['Triple']) | (pbp.EVENT_CD == e['Error']),
#         pbp.EVENT_TX.apply(lambda x: re.split('/|\(|!|E|\.|-|\?|\+', 
#                                                    x)[0]).str[1:],
#         pbp.location)
# 
# # Double. Don't count ground rule doublese because they are uncatchable and
# # runners advancement is predetermined
# pbp['location'] = np.where(pbp.EVENT_CD == e['Double'],
#         pbp.EVENT_TX.apply(lambda x: re.split('/|\(|!|E|\.|-|\?|\+', 
#                                                   x)[0]).str[1:], pbp.location)
# pbp['location'] = np.where(pbp.location.str[0:2] == 'GR', None, pbp.location)
# 
# # Outs in play
# pbp['location'] = np.where(pbp.EVENT_CD == e['Generic out'], 
#    pbp.EVENT_TX.apply(lambda x: re.split('/|\(|!|E|\.|-|\?|\+', x)[0]),
#    pbp.location)
#    
# # Error
# pbp['location'] = np.where(pbp.EVENT_CD == e['Error'], pbp.EVENT_TX.apply(
#         lambda x: re.split('/|\(|!|\.|-|\?|\+', x)[0]).str[1:], pbp.location)
#    
# # Fielder's Choice
# pbp['location'] = np.where(pbp.EVENT_CD == e['Fielder choice'],
#         pbp.EVENT_TX.apply(lambda x: re.split('/|\(|!|E|\.|-|\?|\+', 
#                                                   x)[0]).str[2:], pbp.location)
#    
# # Set empty strings to none
# pbp['location'] = np.where(pbp.location == '', None, pbp.location)
# 
# # Get rid of locations that are not in the following list
# pot_loc = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '46', '64', '56', '65',
#            '34', '43', '78', '87', '89', '98']
# pbp['location'] = np.where(pbp.location.isin(pot_loc), pbp.location, None)
# 
# # Clean locations
# 
# location = pbp.loc[:, ['location']]
# location['count'] = 1
# location = location.groupby(['location']).count()
# location.at['34', 'count'] += location.at['43', 'count']
# location.at['46', 'count'] += location.at['64', 'count']
# location.at['56', 'count'] += location.at['65', 'count']
# location.at['78', 'count'] += location.at['87', 'count']
# location.at['89', 'count'] += location.at['98', 'count']
# location = location.drop(['43', '64', '65', '87', '98'])
# 
# # Get zones. For locations with two positions, probabilistically determine zone
# p = pbp[~pbp.location.isna()]
# for ix, row in p[p.location.str.len() == 2].iterrows():
#     first = location.at[row['location'][0], 'count']
#     second = location.at[row['location'][1], 'count']
#     if first / (first + second) >= random.uniform(0, 1):
#         pbp.at[ix, 'zone'] = row['location'][0]
#     else:
#         pbp.at[ix, 'zone'] = row['location'][0]
# 
# 
# 
# #%%
# # troum001 
# =============================================================================
#%%
roster = pd.read_csv('roster2018.csv')
names = [['Albert', 'Pujols'], ['Mike', 'Trout'], ['David', 'Fletcher']]
#names = [['Mike', 'Trout']]
from initialize_players import initialize_list_to_df
df1 = initialize_list_to_df(roster, names)
pbp = pd.read_csv('all2018.csv', header=None)
fields = pd.read_csv('fields.csv')
pbp.columns = fields.loc[:, 'Header']

#############
#%%
