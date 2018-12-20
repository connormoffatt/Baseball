rm(list=ls())

# Comparing Ruth, Aaron, Bonds, Arod

chapter_path = "C:/Users/conno/Documents/GitHub/Baseball/Analyzing Baseball Data With R/Book - First Edition/Chapter 3 - Traditional Graphics"
setwd(chapter_path)

# (a)
# Read the Lahman "Master.csv" and "batting.csv" data files into R
people <- read.csv("People.csv")
batting <- read.csv("Batting.csv")

# (b)
# Use the getinfo to obtain there data frames for the season batting statistics
# for the great hitters Ty Cobb, Ted Williams, and Pete Rose

# create a function to extract informationi from people database
getinfo <- function(first, last){
  playerline <- subset(people, nameFirst==first & nameLast==last)
  name.code <- as.character(playerline$playerID)
  birthyear <- playerline$birthYear
  birthmonth <- playerline$birthMonth
  birthday <- playerline$birthDay
  byear <- ifelse(birthmonth <= 6, birthyear, birthyear + 1)
  list(name.code=name.code, byear=byear)
}

# get information for the three players
cobb.info <- getinfo("Ty", "Cobb")
williams.info <- getinfo("Ted", "Williams")
rose.info <- getinfo("Pete", "Rose")

# Create a dataframe of batting with the three players
cobb.data <- subset(batting, playerID == cobb.info$name.code)
williams.data <- subset(batting, playerID == williams.info$name.code)
rose.data <- subset(batting, playerID == rose.info$name.code[[1]])

# (c)
# Add the variable Age to each data frame corresponding to the ages of the three
# players
cobb.data$age <- cobb.data$yearID - cobb.info$byear
williams.data$age <- williams.data$yearID - williams.info$byear
rose.data$age <- rose.data$yearID - rose.info$byear[[1]]

# (d)
# Using the plot function, construct a line graph of the cumulative hit totals
# against age for Pete Rose
with(rose.data, plot(age, cumsum(H), type='l', ylab="hits", xlab="Age",
                     main="Pete Rose Hits During Career"), lty=3, lwd=2)

# (e)
# Using the lines function, overlay the cumulative hit totals for Cobb and
# Williams
with(cobb.data, lines(age, cumsum(H), type='l', lty=1, lwd=2))
with(williams.data, lines(age, cumsum(H), type='l', lty=2, lwd=2))
legend("bottomright", legend=c("Cobb", "Williams", "Rose"), lty=1:3, lwd=2, cex=1)

# (f)
# Write a short paragraph summarizing what you have learned about the hitting
# of these three players

# We see that Pete Rose is the all time hits leader, but he played for a
# much longer time than Ty Cobb

