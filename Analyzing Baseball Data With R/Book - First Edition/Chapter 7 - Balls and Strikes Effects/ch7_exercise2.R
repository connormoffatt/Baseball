rm(list=ls())

# Length of Plate Appearances

chapter_path = "C:/Users/conno/Documents/GitHub/Baseball/Analyzing Baseball Data With R/Book - First Edition/Chapter 7 - Balls and Strikes Effects"
setwd(chapter_path)

# (a)
# Calculate the length, in term of pitches, of the average plate appearance
# by batting position sing Retroshet datat for the 2011 season

# Load in play by play data
pbp2011 <- read.csv("all2011.csv")
headers <- read.csv("fields.csv")
names(pbp2011) <- headers$Header

# Get pitch sequences that are actual pitches
pbp2011$pseq <- gsub("[.>123N+*]", "", pbp2011$PITCH_SEQ_TX)
pbp2011$pseq_ct <- nchar(pbp2011$pseq)

# Get batting events and aggregate by batting order
pbp2011bat <- subset(pbp2011, BAT_EVENT_FL=TRUE)
PA.LINEUP <- aggregate(pbp2011$pseq_ct, 
                       by=list(BAT_ORDER_ID=pbp2011$BAT_LINEUP_ID), mean)
  
# (b)
# Does the eighth batter in the National League behave differently than his
# counterpart in the American League?
AL_ID <- c("ANA", "BAL", "BOS", "CHA", "CLE", "DET", "HOU", "KCA", "MIN", "NYA",
           "OAK", "SEA", "TBA", "TEX", "TOR")

pbp2011bat$HOME <- substr(pbp2011bat$GAME_ID, 1, 3)
pbp2011bat$AL <- pbp2011bat$HOME %in% AL_ID

# Aggregate average plate appearances in AL and NL
pbp2011batAL = subset(pbp2011bat, pbp2011bat$HOME %in% AL_ID)
pbp2011batNL = subset(pbp2011bat, !(pbp2011bat$HOME %in% AL_ID))

# Get batting events and aggregate by order for each league
PA.AL.LINEUP <- aggregate(pbp2011batAL$pseq_ct,
                          by=list(BAT_ORDER_ID=pbp2011batAL$BAT_LINEUP_ID), 
                          mean)
PA.NL.LINEUP <- aggregate(pbp2011batNL$pseq_ct,
                          by=list(BAT_ORDER_ID=pbp2011batNL$BAT_LINEUP_ID), 
                          mean)

# There is no discernible difference between the eight hitter in the different
# leagues

# (c)
# Repeat the calculations in (a) and (b) for the 2018 and 2011 seasons and
# comment on any differences between the seasons that you find

# Load in play by play data
pbp2018 <- read.csv("all2018.csv")
headers <- read.csv("fields.csv")
names(pbp2018) <- headers$Header

# Get pitch sequences that are actual pitches
pbp2018$pseq <- gsub("[.>123N+*]", "", pbp2018$PITCH_SEQ_TX)
pbp2018$pseq_ct <- nchar(pbp2018$pseq)

# Get batting events and aggregate by batting order
pbp2018bat <- subset(pbp2018, BAT_EVENT_FL=TRUE)

AL_ID <- c("ANA", "BAL", "BOS", "CHA", "CLE", "DET", "HOU", "KCA", "MIN", "NYA",
           "OAK", "SEA", "TBA", "TEX", "TOR")

pbp2018bat$HOME <- substr(pbp2018bat$GAME_ID, 1, 3)
pbp2018bat$AL <- pbp2018bat$HOME %in% AL_ID

# Aggregate average plate appearances in AL and NL
pbp2018batAL = subset(pbp2018bat, pbp2018bat$HOME %in% AL_ID)
pbp2018batNL = subset(pbp2018bat, !(pbp2018bat$HOME %in% AL_ID))

# Get batting events and aggregate by order for each league
PA.AL.LINEUP.18 <- aggregate(pbp2018batAL$pseq_ct,
                          by=list(BAT_ORDER_ID=pbp2018batAL$BAT_LINEUP_ID), 
                          mean)
PA.NL.LINEUP.18 <- aggregate(pbp2018batNL$pseq_ct,
                          by=list(BAT_ORDER_ID=pbp2018batNL$BAT_LINEUP_ID), 
                          mean)

# Again there is no noticeable difference between the number of pitches seen
# by the eight hitterin both leagues
