rm(list=ls())

# Run Value of Individual Pitches

chapter_path = "C:/Users/conno/Documents/GitHub/Baseball/Analyzing Baseball Data With R/Book - First Edition/Chapter 7 - Balls and Strikes Effects"
setwd(chapter_path)

# (a)
# Calculate the run value of a ball and a strike at any count. For 3-ball and 
# 2-strike conts you need the value of a walk and a strike-out respectively
# (you can calculate them as done for other events in Chapter 5)

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

# Calculate the value of each count
ct.val <- matrix(0, 12, 1)
colnames(ct.val) <- c("Value")
dimnames(ct.val)[[1]] <- c("0-0", "1-0", "2-0", "3-0", "0-1", "1-1", "2-1",
                                "3-1", "0-2", "1-2", "2-2", "3-2")

d00 <- subset(data2011, BALLS_CT==0 & STRIKES_CT==0)
d10 <- subset(data2011, BALLS_CT==1 & STRIKES_CT==0)
d20 <- subset(data2011, BALLS_CT==2 & STRIKES_CT==0)
d30 <- subset(data2011, BALLS_CT==3 & STRIKES_CT==0)
d01 <- subset(data2011, BALLS_CT==0 & STRIKES_CT==1)
d11 <- subset(data2011, BALLS_CT==1 & STRIKES_CT==1)
d21 <- subset(data2011, BALLS_CT==2 & STRIKES_CT==1)
d31 <- subset(data2011, BALLS_CT==3 & STRIKES_CT==1)
d02 <- subset(data2011, BALLS_CT==0 & STRIKES_CT==2)
d12 <- subset(data2011, BALLS_CT==1 & STRIKES_CT==2)
d22 <- subset(data2011, BALLS_CT==2 & STRIKES_CT==2)
d32 <- subset(data2011, BALLS_CT==3 & STRIKES_CT==2)

# Calculate value for each count
ct.val["0-0", "Value"] = mean(d00$RUNS.VALUE)
ct.val["1-0", "Value"] = mean(d10$RUNS.VALUE)
ct.val["2-0", "Value"] = mean(d20$RUNS.VALUE)
ct.val["3-0", "Value"] = mean(d30$RUNS.VALUE)
ct.val["0-1", "Value"] = mean(d01$RUNS.VALUE)
ct.val["1-1", "Value"] = mean(d11$RUNS.VALUE)
ct.val["2-1", "Value"] = mean(d21$RUNS.VALUE)
ct.val["3-1", "Value"] = mean(d31$RUNS.VALUE)
ct.val["0-2", "Value"] = mean(d02$RUNS.VALUE)
ct.val["1-2", "Value"] = mean(d12$RUNS.VALUE)
ct.val["2-2", "Value"] = mean(d22$RUNS.VALUE)
ct.val["3-2", "Value"] = mean(d32$RUNS.VALUE)

# Calculate the value of balls and strikes in each count
bs.val <- matrix(0, 12, 2)
dimnames(bs.val)[[2]] = c("Strike", "Ball")
dimnames(bs.val)[[1]] <- c("0-0", "1-0", "2-0", "3-0", "0-1", "1-1", "2-1", 
                           "3-1", "0-2", "1-2", "2-2", "3-2")

# Mean value of strikeout
d.strikeout <- subset(data2011, EVENT_CD==3)
strikeout_val <- mean(d.strikeout$RUNS.VALUE)

# Mean value of walk
d.walk <- subset(data2011, EVENT_CD==14)
walk_val <- mean(d.walk$RUNS.VALUE)

# Calculate Values of different pitches for Strikes
bs.val["0-0", "Strike"] = round(ct.val["0-1", "Value"] - ct.val["0-0", "Value"], 2)
bs.val["1-0", "Strike"] = round(ct.val["1-1", "Value"] - ct.val["1-0", "Value"], 2)
bs.val["2-0", "Strike"] = round(ct.val["2-1", "Value"] - ct.val["2-0", "Value"], 2)
bs.val["3-0", "Strike"] = round(ct.val["3-1", "Value"] - ct.val["3-0", "Value"], 2)

bs.val["0-1", "Strike"] = round(ct.val["0-2", "Value"] - ct.val["0-1", "Value"], 2)
bs.val["1-1", "Strike"] = round(ct.val["1-2", "Value"] - ct.val["1-1", "Value"], 2)
bs.val["2-1", "Strike"] = round(ct.val["2-2", "Value"] - ct.val["2-1", "Value"], 2)
bs.val["3-1", "Strike"] = round(ct.val["3-2", "Value"] - ct.val["3-1", "Value"], 2)

bs.val["0-2", "Strike"] = round(strikeout_val - ct.val["0-2", "Value"], 2)
bs.val["1-2", "Strike"] = round(strikeout_val - ct.val["1-2", "Value"], 2)
bs.val["2-2", "Strike"] = round(strikeout_val - ct.val["2-2", "Value"], 2)
bs.val["3-2", "Strike"] = round(strikeout_val - ct.val["3-2", "Value"], 2)

# Calculate Values of different pitches for Balls
bs.val["0-0", "Ball"] = round(ct.val["1-0", "Value"] - ct.val["0-0", "Value"], 2)
bs.val["1-0", "Ball"] = round(ct.val["2-0", "Value"] - ct.val["1-0", "Value"], 2)
bs.val["2-0", "Ball"] = round(ct.val["3-0", "Value"] - ct.val["2-0", "Value"], 2)
bs.val["3-0", "Ball"] = round(walk_val - ct.val["3-0", "Value"], 2)

bs.val["0-1", "Ball"] = round(ct.val["1-1", "Value"] - ct.val["0-1", "Value"], 2)
bs.val["1-1", "Ball"] = round(ct.val["2-1", "Value"] - ct.val["1-1", "Value"], 2)
bs.val["2-1", "Ball"] = round(ct.val["3-1", "Value"] - ct.val["2-1", "Value"], 2)
bs.val["3-1", "Ball"] = round(walk_val - ct.val["3-1", "Value"], 2)

bs.val["0-2", "Ball"] = round(ct.val["1-2", "Value"] - ct.val["0-2", "Value"], 2)
bs.val["1-2", "Ball"] = round(ct.val["2-2", "Value"] - ct.val["1-2", "Value"], 2)
bs.val["2-2", "Ball"] = round(ct.val["3-2", "Value"] - ct.val["2-2", "Value"], 2)
bs.val["3-2", "Ball"] = round(walk_val - ct.val["3-2", "Value"], 2)

# (b)
# Compare your values to the ones proposed by John Walsh in the article 
# www.hardballtimes.com/main/article/searching-for-the-games-best-pitch

# The values are similar to those in the fangraphs article. They possibly
# have a smaller magnitude

