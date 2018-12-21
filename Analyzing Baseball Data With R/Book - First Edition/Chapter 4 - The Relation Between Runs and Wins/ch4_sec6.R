rm(list=ls())

chapter_path = "C:/Users/conno/Documents/GitHub/Baseball/Analyzing Baseball Data With R/Book - First Edition/Chapter 4 - The Relation Between Runs and Wins"
setwd(chapter_path)

# Good and Bad Predictions By the Pythagorean Formula

# load in teams table and display the last 5 rows with tail
teams <- read.csv("Teams.csv")

# Create data frame with a reduced number of attributes
keep_col <-  c("teamID", "yearID", "lgID", "G", "W", "L", "R", "RA")
myteams <- subset(teams, yearID > 2000)[, keep_col]

# Calculate run differential and winning percentage
myteams$RD <- with(myteams, R - RA)
myteams$Wpct <-  with(myteams, W / (W + L))

# Calculate pythagorean win percentage
myteams$pytWpct <- with(myteams, R^2 / (R^2 + RA^2))

# Calculate residuals of pytWpct
myteams$pytResiduals <- myteams$Wpct - myteams$pytWpct

# load in 2011 game data
gl2011 <- read.table("gl2011.txt", sep=",")
glheaders <- read.csv("game_log_header.csv")
names(gl2011) = names(glheaders)

# Get Boston games data frame
BOS2011 <- subset(gl2011, HomeTeam=="BOS" | VisitingTeam=="BOS")[
  , c("VisitingTeam", "HomeTeam", "VisitorRunsScored", "HomeRunsScore")]

#  Calculate score differential and wins
BOS2011$ScoreDiff <- with(BOS2011, ifelse(
  HomeTeam=="BOS", HomeRunsScore - VisitorRunsScored,
  VisitorRunsScored - HomeRunsScore))
BOS2011$W <- BOS2011$ScoreDiff > 0 

# Aggregate score difference for wins and losses
aggregate(abs(BOS2011$ScoreDiff), list(W=BOS2011$W), summary)

# Check pythagorean performance

# load in results dataframe
results <- gl2011[, c("VisitingTeam", "HomeTeam", "VisitorRunsScored", 
                      "HomeRunsScore")]

# add winner and run differential
results$winner <- ifelse(results$HomeRunsScore > results$VisitorRunsScored,
                         as.character(results$HomeTeam),
                         as.character(results$VisitingTeam))
results$diff <- abs(results$HomeRunsScore - results$VisitorRunsScored)

# create dataframe of one run games
onerungames <- subset(results, diff==1)
onerunwins <- as.data.frame(table(onerungames$winner))
names(onerunwins) <- c("teamID", "onerunW")

# use my teams to calculate pythagorean residuals. Update LAA to ANA
teams2011 <- subset(myteams, yearID==2011)
teams2011[teams2011$teamID == "LAA", "teamID"] <- "ANA"
teams2011 <- merge(teams2011, onerunwins)

# display scatter of one run wins v. residuals
plot(teams2011$onerunW, teams2011$pytResiduals, xlab="Games Won by One Run",
     ylab="Pythagorean Residual", 
     main="Analyzing Pythagorean Win Performance with One Run Games")

# Use Identify to get largest and smallest
identify(teams2011$onerunW, teams2011$pytResiduals, labels=teams2011$teamID, 
         n=2)

# Create data frame of top closers
pitching <- read.csv("pitching.csv")
top_closers <- subset(pitching, GF > 50 & ERA < 2.5)[, 
                      c("playerID", "yearID", "teamID")]

# Merge top closers with myteams and get summary of pythagrean residuals
teams_top_closers <- merge(top_closers, myteams)
summary(teams_top_closers$pytResiduals)