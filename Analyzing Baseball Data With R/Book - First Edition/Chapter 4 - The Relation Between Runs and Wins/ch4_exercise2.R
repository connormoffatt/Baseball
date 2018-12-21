rm(list=ls())

# Pythagorean Residuals for Poor and Great Teams in the 19th Century

# As baseball was evolving into its ultimate form, nineteenth century leagues
# often featured abysmal teams that did not even succeed in finishing their
# season, as well as some dominant clubs

# (a)
# Fit a Pythagorean formula model to the run-differential, win-loss data for
# teams who played in the 19th century.
teams <- read.csv("Teams.csv")

# Create data frame with a reduced number of attributes
keep_col = c("teamID", "yearID", "lgID", "G", "W", "L", "R", "RA")
myteams <- subset(teams, yearID >= 1800 & yearID <= 1899)[, keep_col]

# Calculate pythagorean win percentage
myteams$pytWpct <- with(myteams, R^2 / (R^2 + RA^2))

# (b)
# By inspecting the residual plot of your fitted model form (a), did the great
# and poor eams in the 19th century do better or worse than one would expect
# on the basis of their run differentials

# Calculate run differential and winning percentage
myteams$RD = with(myteams, R - RA)
myteams$Wpct = with(myteams, W / (W + L))

# Calculate residuals of pytWpct
myteams$pytResiduals <- myteams$Wpct - myteams$pytWpct

plot(myteams$RD, myteams$pytResiduals, xlab="Run Differential", ylab="Residual",
     main="Pythagorean Win Residuals During 19th Century")

# The Pythagorean formula does not perform better or worse than expected for 
# teams that are abysmal or dominant
