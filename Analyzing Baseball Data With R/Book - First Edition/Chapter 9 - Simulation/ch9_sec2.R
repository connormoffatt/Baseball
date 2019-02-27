rm(list=ls())

chapter_path = "C:/Users/conno/Documents/GitHub/Baseball/Analyzing Baseball Data With R/Book - First Edition/Chapter 9 - Simulation"
setwd(chapter_path)

rm(list=ls())

# Simulating a Half Inning

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

# Get only batting events
data2011c <- subset(data2011c, BAT_EVENT_FL == TRUE)

# If there are three outs just make the state equalto 3

data2011c$NEW.STATE <- recode(data2011c$NEW.STATE, 
                          "c('000 3', '100 3', '010 3', '001 3', 
                              '110 3', '101 3', '011 3', '111 3')='3'")

# Get frequency matrix
T.matrix <- with(data2011c, table(STATE, NEW.STATE))

# Turn into a probability matrix
P.matrix <- prop.table(T.matrix, 1)

# Add row that corresponds to three outs. Cannot transition out of this
P.matrix <- rbind(P.matrix, c(rep(0, 24), 1))

# Number of runs is equal to. Quantity (1 + # runners at end of play + # outs
# at end of play) MINUS Quantity (# runners at beginning of play + # outs
# at beginning of play)

# Create function to calculate runs for each transtion. Note there may be some
# large numbers and negative numbers for transitions taht do not actually exist
# e.g. 0 outs 0 runners to 3 outs

count.runners.outs <- function(s)
  sum(as.numeric(strsplit(s, "")[[1]]), na.rm=TRUE)
runners.outs <- sapply(dimnames(T.matrix)[[1]], count.runners.outs)[-25]
R <- outer(runners.outs + 1, runners.outs, FUN="-")
dimnames(R)[[1]] <- dimnames(T.matrix[[1]])[-25]
dimnames(R)[[2]] <- dimnames(T.matrix[[1]])[-25]
R <- cbind(R, rep(0, 24))

# Write function to simulate a half inning
simulate.half.inning <- function(P, R, start=1){
  s <- start
  path <- NULL
  runs <- 0
  while(s < 25){
    s.new <- sample(1:25, 1, prob=P[s,])
    path <- c(path, s.new)
    runs <- runs + R[s, s.new]
    s <- s.new
  }
  runs
}

# Simulate 10,000 half innings
RUNS <- replicate(10000, simulate.half.inning(T.matrix, R))

table(RUNS)
mean(RUNS)

# We can calculate a Run Expectancy Matrix from batting events using
# different starting states

# For simplicity we will not enter all the code here

# We can use matrix multiplication to see the state after 3 plate appearances
P.matrix3 <- P.matrix %*% P.matrix %*% P.matrix
sortedP <- sort(round(P.matrix3["000 0",], 3), decreasing=TRUE)
head(data.frame(Prob=sortedP))

# Fundamental Matrix N of an Absorbing Markov Chain.
# For entry n_ij of N gives the expected number of times that the
# process is in the transient state s_j if it is started in the transiet
# state s_i

Q <- P.matrix[-25, -25]
N <- solve(diag(rep(1, 24)) - Q)

# Other examples looking at the matrix N
