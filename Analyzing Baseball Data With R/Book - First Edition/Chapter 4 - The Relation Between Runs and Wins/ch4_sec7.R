rm(list=ls())

chapter_path = "C:/Users/conno/Documents/GitHub/Baseball/Analyzing Baseball Data With R/Book - First Edition/Chapter 4 - The Relation Between Runs and Wins"
setwd(chapter_path)

# How Many Runs for a Win

# Calculate partial derivative of pythagorean formula in wins
D(expression(G * R^2 / (R^2 + RA^2)), "R")

# Create function to reflect this partial derivative for runs per win
# RS and RA are runs scored per game and runs allowed per game
IR <- function(RS, RA){
  round((RS^2 + RA^2)^2 / (2 * RS * RA^2), 1)
}

# Create grid to determine how many runs are equal to a win given the 
# average runs allowed and average runs scored
IRtable <- expand.grid(RS=seq(3,6,0.5), RA=seq(3,6,0.5))
rbind(head(IRtable), tail(IRtable))

# Calculate incremental runs table and display
IRtable$IRW <- IR(IRtable$RS, IRtable$RA)
xtabs(IRW  ~ RS + RA, data=IRtable)
