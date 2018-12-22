rm(list=ls())

chapter_path = "C:/Users/conno/Documents/GitHub/Baseball/Analyzing Baseball Data With R/Book - First Edition/Chapter 5 - Value of Plays Using Run Expectancy"
setwd(chapter_path)

# Position in Batting Lineup

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

#--------------------------------------------------------

Roster <- read.csv("roster2011.csv")
albert.id <- subset(Roster, First.Name=="Albert" & Last.Name=="Pujols")$Player.ID
albert.id <- as.character(albert.id)

albert <- subset(data2011, BAT_ID == albert.id & BAT_EVENT_FL == TRUE)

#--------------------------------------------------------

# Get all batting events
data2011b <- subset(data2011, BAT_EVENT_FL==TRUE)

# For each player get their plate appearances, run value after, and run value
# before
runs.sums <- aggregate(data2011b$RUNS.VALUE, list(data2011b$BAT_ID), sum)
runs.pa <- aggregate(data2011b$RUNS.VALUE, list(data2011b$BAT_ID), length)
runs.start <- aggregate(data2011b$RUNS.STATE, list(data2011b$BAT_ID), sum)

names(runs.sums) <- c("Batter", "Runs")
names(runs.pa) <- c("Batter", "PA")
names(runs.start) <- c("Batter", "Runs.Start")

runs <- merge(runs.sums, runs.pa)
runs <- merge(runs, runs.start)

# Get batters with more tahn 400 plate appearances
runs400 <- subset(runs, PA >= 400)

# Plot run opportunities vs. runs created
with(runs400, plot(Runs.Start, Runs))
abline(h=0)

# Add text to top players. >= 40 runs
runs400.top <- subset(runs400, Runs >= 40)
roster2011 <- read.csv("roster2011.csv")
runs400.top <- merge(runs400.top, roster2011, by.x="Batter", by.y="Player.ID")
with(runs400.top, text(Runs.Start, Runs, Last.Name, pos=1, cex=0.75))

#---------------------------------------------------------

# Create function to obtain batting position
get.batting.pos <- function(batter){
  TB <- table(subset(data2011, BAT_ID==batter)$BAT_LINEUP_ID)
  names(TB)[TB == max(TB)][1]
}

# Get position for every batter
position <- sapply(as.character(runs400$Batter), get.batting.pos)

# Plot
with(runs400, plot(Runs.Start, Runs, type='n'))
with(runs400, lines(lowess(Runs.Start, Runs)))
abline(h=0)
with(runs400, text(Runs.Start, Runs, position, cex=0.75))

# Place dot where Pujols is
AP <- subset(runs400, Batter==albert.id)
points(AP$Runs.Start, AP$Runs, pch=19, cex=3)
