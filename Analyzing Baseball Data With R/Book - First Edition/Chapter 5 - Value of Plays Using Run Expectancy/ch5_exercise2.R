rm(list=ls())

# There are three different ways for a runner to get on base, a single, BB,
# HBP. Different outcomes ahve different values. Use run values based on 
# data from the 2011 season to compare the benefit of BB, HBP, and single
# when there is a single runner on first

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
data2011$RUNS.SCORED <- with(data2011, (BAT_DEST_ID > 3) + (RUN1_DEST_ID > 3)
                             + (RUN2_DEST_ID > 3) + (RUN3_DEST_ID > 3))

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

# Calculate the runs for the remainder of the inning. Typo in Book
data2011$RUNS.ROI <- with(data2011, MAX.RUNS - RUNS)

# --------------------------------------------------------

# Create Binary Variable to determine if runner is on a base before play
RUNNER1 <- ifelse(as.character(data2011[,"BASE1_RUN_ID"]) == "", 0, 1)
RUNNER2 <- ifelse(as.character(data2011[,"BASE2_RUN_ID"]) == "", 0, 1)
RUNNER3 <- ifelse(as.character(data2011[,"BASE3_RUN_ID"]) == "", 0, 1)

# Create function to get the current state dependent on baserunners and outs
get.state <- function(r1, r2, r3, outs){
  runners <- paste(r1, r2, r3, sep="")
  paste(runners, outs)
}

# Add states to 2011 data
data2011$STATE <- get.state(RUNNER1, RUNNER2, RUNNER3, data2011$OUTS_CT)

# Create Binary Variable to determine if a runner is on a base after play
NRUNNER1 <- with(data2011, as.numeric(RUN1_DEST_ID == 1 |
                                        BAT_DEST_ID == 1))
NRUNNER2 <- with(data2011, as.numeric(RUN1_DEST_ID == 2 |
                                        RUN2_DEST_ID == 2 | BAT_DEST_ID == 2))
NRUNNER3 <- with(data2011, as.numeric(RUN1_DEST_ID == 3 |
                                        RUN2_DEST_ID == 3 | RUN3_DEST_ID == 3 | BAT_DEST_ID == 3))

# Get number of outs at the end of play
NOUTS <- with(data2011, OUTS_CT + EVENT_OUTS_CT)

# Get the new state
data2011$NEW.STATE <- get.state(NRUNNER1, NRUNNER2, NRUNNER3, NOUTS)

# Reduce dataframe to when states change or runs score
data2011 <- subset(data2011, (STATE != NEW.STATE) | (RUNS.SCORED) > 0)

# filter out half innings that are walk-offs because they are not complete
# innings

library(plyr)
data.outs <- ddply(data2011, .(HALF.INNING), summarize, 
                   Outs.Inning=sum(EVENT_OUTS_CT))
data2011 <- merge(data2011, data.outs)
data2011c <- subset(data2011, Outs.Inning==3)

# Calculate the expected number of runs for each element of the matrix
RUNS <- with(data2011c, aggregate(RUNS.ROI, list(STATE), mean))

# Display matrix. First order by out then create matrix

# Get the 5th character to the 5th character in the string
RUNS$OUTS <- substr(RUNS$Group.1, 5, 5)
RUNS <- RUNS[order(RUNS$OUTS),]
RUNS.out <- matrix(round(RUNS$x, 2), 8, 3)
dimnames(RUNS.out)[[2]] <- c("0 outs", "1 out", "2 outs")
dimnames(RUNS.out)[[1]] <- c("000", "001", "010", "011", "100", "101", "110", "111")

#------------------------------------------------------

# Calculate the run value for each play

# Calculate a potential runs matrix. We know that with 3 outs no more runs can
# be scored
RUNS.POTENTIAL <- matrix(c(RUNS$x, rep(0, 8)), 32, 1)
dimnames(RUNS.POTENTIAL)[[1]] <- c(RUNS$Group.1, "000 3", "001 3", "010 3",
                                   "011 3", "100 3", "101 3", "110 3", "111 3")

# Calculate Runs Value of State Before Play
data2011$RUNS.STATE <- RUNS.POTENTIAL[data2011$STATE,]

# Calculate Runs Value of State After Play
data2011$RUNS.NEW.STATE <- RUNS.POTENTIAL[data2011$NEW.STATE,]

# Calculate Runs Value
data2011$RUNS.VALUE <- data2011$RUNS.NEW.STATE - data2011$RUNS.STATE + 
  data2011$RUNS.SCORED

# Walk -> 14
# Hit By Pitch -> 16
# Single -> 20

# Get data frame where it is just a runner on first
data <- data2011[data2011$STATE=="100 0" | data2011$STATE=="100 1" |
                   data2011$STATE=="100 2",]

# Mean value of Walk
d.walk <- subset(data, EVENT_CD==14)
mean.walk <- mean(d.walk$RUNS.VALUE)

# Mean value of Hit By Pitch
d.hbp <- subset(data, EVENT_CD==16)
mean.hbp <- mean(d.hbp$RUNS.VALUE)

# Mean value of Single
d.single <- subset(data, EVENT_CD==20)
mean.single <- mean(d.single$RUNS.VALUE)

# For runner on first base
# walk: 0.365
# hbp: 0.383
# single: 0.440
