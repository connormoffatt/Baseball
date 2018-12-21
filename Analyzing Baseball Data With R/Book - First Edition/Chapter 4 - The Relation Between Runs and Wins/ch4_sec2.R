rm(list=ls())

chapter_path = "C:/Users/conno/Documents/GitHub/Baseball/Analyzing Baseball Data With R/Book - First Edition/Chapter 4 - The Relation Between Runs and Wins"
setwd(chapter_path)

# The Teams Table in the Lahman Database

# load in teams table and display the last 5 rows with tail
teams <- read.csv("Teams.csv")
tail(team)

# Create data frame with a reduced number of attributes
keep_col = c("teamID", "yearID", "lgID", "G", "W", "L", "R", "RA")
myteams <- subset(teams, yearID > 2000)[, keep_col]
tail(myteams)

# Calculate run differential and winning percentage
myteams$RD = with(myteams, R - RA)
myteams$Wpct = with(myteams, W / (W + L))

# Scatter plot of run differential and winning percentage
plot(myteams$RD, myteams$Wpct, main="Relationship Between RD and Winning %",
     xlab="Run Differential", ylab="Winning Percentage")
