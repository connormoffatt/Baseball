rm(list=ls())

chapter_path = "C:/Users/conno/Documents/GitHub/Baseball/Analyzing Baseball Data With R/Book - First Edition/Chapter 5 - Value of Plays Using Run Expectancy"
setwd(chapter_path)

# Runs Scored in the Remainder of an Inning

# read in 2011 play by play data
data2011 <- read.csv("all2011.csv")
fields <- read.csv("fields.csv")
names(data2011) <- fields[,"Header"]

# We want to calculate the runs scored for the remaining of the inning

# First calculate the runs at a given time
data2011$RUNS <- with(data2011, AWAY_SCORE_CT + HOME_SCORE_CT)

# Create a unique ID for each half inning
data2011$HALF.INNING <- with(data2011, paste(GAME_ID, INN_CT, BAT_HOME_ID))

# Now we will calculate how many runs were scored at the end of the inning

# Calculate the number of runs scored during each play
data2011$RUNS_SCORED <- with(data2011, (BAT_DEST_ID > 3) + (RUN1_DEST_ID > 3)
                             + (RUN2_DEST_ID > 3) +(RUN3_DEST_ID > 3))

# Aggregate to sum the runs scored on each play to determine the number of
# runs scored in the half inning
RUNS.SCORED.INNING <- aggregate(data2011$RUNS.SCORED, 
                                list(HALF.INNING=data2011$HALF.INNING), sum)

# Find the total game runs at the beginning of the inning with "[" function 
RUNS.SCORED.START <- aggregate(data2011$RUNS,
                               list(HALF.INNING=data2011$HALF.INNING), "[", 1)

# Get the maximum number of runs in the half inning
MAX <- data.frame(HALF.INNING=RUNS.SCORED.START$HALF.INNING)
MAX$x <- RUNS.SCORED.INNING$x + RUNS.SCORED.START$x

# Merge the data and name the column
data2011 <- merge(data2011, MAX)
names(data2011)[ncol(data2011)] <- "MAX.RUNS"

# Calculate the runs for the remainder of the inning
data2011$RUNS.ROI <- with(data2011, MAX.RUNS - RUNS)