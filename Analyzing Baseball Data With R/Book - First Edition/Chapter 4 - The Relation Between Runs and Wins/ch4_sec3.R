rm(list=ls())

chapter_path = "C:/Users/conno/Documents/GitHub/Baseball/Analyzing Baseball Data With R/Book - First Edition/Chapter 4 - The Relation Between Runs and Wins"
setwd(chapter_path)

# The Teams Table in the Lahman Database

# load in teams table and display the last 5 rows with tail
teams <- read.csv("Teams.csv")

# Create data frame with a reduced number of attributes
keep_col = c("teamID", "yearID", "lgID", "G", "W", "L", "R", "RA")
myteams <- subset(teams, yearID > 2000)[, keep_col]

# Calculate run differential and winning percentage
myteams$RD = with(myteams, R - RA)
myteams$Wpct = with(myteams, W / (W + L))

# Calculate the linear regression between run differential and win %
linfit <- lm(Wpct ~ RD, data=myteams)

# Scatter plot of run differential and winning percentage
plot(myteams$RD, myteams$Wpct, main="Relationship Between RD and Winning %",
     xlab="Run Differential", ylab="Winning Percentage")

# Plot line of linear fit
abline(a=coef(linfit)[1], b=coef(linfit)[2], lwd=2)

# Calculate prediction and residuals from linear model
myteams$linWpct <- predict(linfit)
myteams$linResiduals <- residuals(linfit)

# plot residuals from above
plot(myteams$RD, myteams$linResiduals, xlab="Run Differential", ylab="resdiual")
abline(h=0, lty=3)
points(c(68, 88), c(0.0749, -0.0733), pch=19)
text(68, 0.0749, "LAA 08", pos=4, cex=0.8)
text(88, -0.0733, "CLE 06", pos=4, cex=0.8)

# Find root mean squared error
linRMSE <- sqrt(mean(myteams$linResiduals ^ 2))

# Check one and two standard deviations
nrow(subset(myteams, abs(linResiduals) < linRMSE)) / nrow(myteams)
nrow(subset(myteams, abs(linResiduals) < 2 * linRMSE)) / nrow(myteams)


