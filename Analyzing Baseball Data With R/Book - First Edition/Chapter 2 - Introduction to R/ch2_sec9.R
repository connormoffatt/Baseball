rm(list=ls())

# Splitting, Applying, and Combining Data
library(Lahman)

# sapply function and plypr package is useful modifying dataframes

# read in batting data from the 60s
Batting <- read.csv("Batting.csv")
Batting.60 <- subset(Batting, yearID >= 1960 & yearID < 1970)

# Create function to retrive number of home runs for a player ID
compute.hr <- function(pid) {
  d <- subset(Batting.60, playerID == pid)
  sum(d$HR)
}

# The function sapply is useful for repeating an operation over a set of values
# in a vector
players <- unique(Batting.60$playerID)
S <- sapply(players, compute.hr)

# Create a new dataframe R that has players and homeruns. Reorder by HR
R <- data.frame(Players=players, HR=S)
R <- R[order(R$HR, decreasing=TRUE),]
head(R)

# Use plypr to get all batters with at least 5000 at bats
library(plyr)
# Batting is the dataframe to work on, playerID is the grouping attribute,
# we are summarizing data, Career.AB is how we are summamring. na.rm=TRUE means
# to remove the NA values. This first datframe is only the players and career AB
dataframe.AB <- ddply(Batting, .(playerID), summarize, 
                      Career.AB=sum(AB, na.rm=TRUE))

# merge with original dataframe and get subset with more than 5000 ABs
Batting <- merge(Batting, dataframe.AB, by="playerID")
Batting.5000 <- subset(Batting, Career.AB >= 5000)

# Create function that creates a career AB, HR, SO dataframe
ab.hr.so <- function(d){
  c.AB <- sum(d$AB, na.rm=TRUE)
  c.HR <- sum(d$HR, na.rm=TRUE)
  c.SO <- sum(d$SO, na.rm=TRUE)
  data.frame(AB=c.AB, HR=c.HR, SO=c.SO)
}

# Apply function to hank aaron
aaron <- subset(Batting.5000, playerID=="aaronha01")
ab.hr.so(aaron)

# Apply to every player with more than 5000 at bats
d.5000 <- ddply(Batting.5000, .(playerID), ab.hr.so)
head(d.5000)

# plot scatter plot and smoothing curuve to see association between home run
# rate and strikeout rate
with(d.5000, plot(HR/AB, SO/AB))
with(d.5000, lines(lowess(HR/AB, SO/AB)))






