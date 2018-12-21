rm(list=ls())

chapter_path = "C:/Users/conno/Documents/GitHub/Baseball/Analyzing Baseball Data With R/Book - First Edition/Chapter 4 - The Relation Between Runs and Wins"
setwd(chapter_path)

# The Exponent in the Pythagorean Formula

# We want to find a general exponenent for the pythagorean formula
# we will solve for the exponent k
# take log of both sides to get log(W/L) = k*log(R/RA)

# load in teams table and display the last 5 rows with tail
teams <- read.csv("Teams.csv")

# Create data frame with a reduced number of attributes
keep_col <-  c("teamID", "yearID", "lgID", "G", "W", "L", "R", "RA")
myteams <- subset(teams, yearID > 2000)[, keep_col]

# Calculate appropraite log values
myteams$logWratio <-  log(myteams$W / myteams$L)
myteams$logRratio <-  log(myteams$R / myteams$RA)

# Calculate linear regression intercept = 0 for k
pytFit <- lm(logWratio ~ 0 + logRratio, data=myteams)