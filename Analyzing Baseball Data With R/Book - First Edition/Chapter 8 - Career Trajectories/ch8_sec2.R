rm(list=ls())

chapter_path = "C:/Users/conno/Documents/GitHub/Baseball/Analyzing Baseball Data With R/Book - First Edition/Chapter 8 - Career Trajectories"
setwd(chapter_path)

Batting <- read.csv("Batting.csv")
People <- read.csv("People.csv")

mantle.info <- subset(People, nameFirst=="Mickey" & nameLast=="Mantle")
mantle.id <- as.character(mantle.info$playerID)

# Convert missing values to zero with recode
library(car)
Batting$SF <- recode(Batting$SF, "NA = 0")
Batting$HBP <- recode(Batting$HBP, "NA = 0")

# MLB defines a player's age as his age on June 30 of that season
# Function to get a player's Birthyear defined by MLB
get.birthyear <- function(player.id){
  playerline <- subset(People, playerID==player.id)
  birthyear <- playerline$birthYear
  birthmonth <- playerline$birthMonth
  ifelse(birthmonth < 7, birthyear, birthyear + 1)
}

# Check function with Mantle
get.birthyear(mantle.id)

# Get batting statistics by player id
get.stats <- function(player.id){
  d <- subset(Batting, playerID==player.id)
  byear <- get.birthyear(player.id)
  d$Age <- d$yearID - byear
  d$SLG <- with(d, (H - X2B - X3B - HR + 2*X2B + 3*X3B + 4*HR) / AB)
  d$OBP <- with(d, (H + BB) / (H + AB + BB + SF))
  d$OPS <- with(d, SLG + OBP)
  d
}

# Read in Mantle Stats
Mantle <- get.stats(mantle.id)

# Plot in Mantle Stats
with(Mantle, plot(Age, OPS, cex=1.5, pch=19, main="Mickey Mantle OPS by Age"))

# Create a function that returns a quadratic fit as well as max and peak age
fit.model <- function(d){
  fit <- lm(d$OPS ~ I(Age - 30) + I((Age-30)^2), data=d)
  b <- coef(fit)
  Age.max <- 30 - b[2] / b[3] / 2
  Max <- b[1] - b[2]^2 / b[3] / 4
  list(fit=fit, Age.max=Age.max, Max=Max)
}

# Fit Mantles dataframe
F2 <- fit.model(Mantle)

# Use predict function to plot model
lines(Mantle$Age, predict(F2$fit, Age=Mantle$Age), lwd=3)
abline(v=F2$Age.max, lwd=3, lty=2, col="grey")
abline(h=F2$Max, lwd=3, lty=2, col="grey")
text(29, 0.72, "Peak Age", cex=2)
text(20, 1, "Max", cex=2)

# Get summary of model fit
summary(F2$fit)

# R^2 is the like percent variability that can be attributed to model
# Residual standard error. ~2/3 of residuals fall within the standard error