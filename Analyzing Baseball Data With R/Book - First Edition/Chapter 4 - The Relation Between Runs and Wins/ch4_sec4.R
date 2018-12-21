rm(list=ls())

chapter_path = "C:/Users/conno/Documents/GitHub/Baseball/Analyzing Baseball Data With R/Book - First Edition/Chapter 4 - The Relation Between Runs and Wins"
setwd(chapter_path)

# The Pythagorean Formula for Winning Percentage

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

# calculate RMSE
sqrt(mean(myteams$pytResiduals ^ 2))
