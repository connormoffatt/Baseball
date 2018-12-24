import pandas as pd
# Length of Plate Appearances

# (a)
# Calculate the length, in term of pitches, of the average plate appearance
# by batting position sing Retroshet datat for the 2011 season

# Load in play by play data
pbp2011 = pd.read_csv("all2011.csv")
headers = pd.read_csv("fields.csv")
pbp2011.columns = headers.Header

# Get pitch sequences that are actual pitches
pbp2011['pseq'] = pbp2011['PITCH_SEQ_TX'].str.replace(r'[.>123N+*]', '',
       regex=True)
pbp2011['pseq_ct'] = pbp2011['pseq'].str.len()

# Get batting events and aggregate by batting order
pbp2011bat = pbp2011[pbp2011.BAT_EVENT_FL == 'T']
PA_LINEUP = pbp2011bat.loc[:, ['pseq_ct', 'BAT_LINEUP_ID']].groupby(
        ['BAT_LINEUP_ID']).mean().loc[:, 'pseq_ct']

# (b)
# Does the eighth batter in the National League behave differently than his
# counterpart in the American League?
AL_ID = ["ANA", "BAL", "BOS", "CHA", "CLE", "DET", "HOU", "KCA", "MIN", "NYA",
           "OAK", "SEA", "TBA", "TEX", "TOR"]

# Sort into an AL data frame and an NL data frame
pbp2011bat['HOME'] = pbp2011bat.GAME_ID.str.slice(0,3)
pbp2011bat['AL'] = pbp2011bat.HOME.isin(AL_ID)

pbp2011batAL = pbp2011bat[pbp2011bat.HOME.isin(AL_ID)]
pbp2011batNL = pbp2011bat[~pbp2011bat.HOME.isin(AL_ID)]

# Get batting events and aggregate by order for each league
PA_AL_LINEUP = pbp2011batAL.loc[:, ['pseq_ct', 'BAT_LINEUP_ID']].groupby(
        ['BAT_LINEUP_ID']).mean().loc[:, 'pseq_ct']

PA_NL_LINEUP = pbp2011batNL.loc[:, ['pseq_ct', 'BAT_LINEUP_ID']].groupby(
        ['BAT_LINEUP_ID']).mean().loc[:, 'pseq_ct']

# There is no discernible difference between the eight hitter in the different
# leagues

# (c)
# Repeat the calculations in (a) and (b) for the 2018 and 2011 seasons and
# comment on any differences between the seasons that you find

# For simplicity, we will not write this code in python since the analysis
# has already been performed in R

# Again there is no noticeable difference between the number of pitches seen
# by the eight hitterin both leagues
