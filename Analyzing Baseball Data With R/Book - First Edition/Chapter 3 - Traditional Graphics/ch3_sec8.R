rm(list=ls())

# Comparing Ruth, Aaron, Bonds, Arod

chapter_path = "C:/Users/conno/Documents/GitHub/Baseball/Analyzing Baseball Data With R/Book - First Edition/Chapter 3 - Traditional Graphics"
setwd(chapter_path)

# read in People database in Lahman
people <- read.csv("People.csv")

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

# get information for the four players
ruth.info <- getinfo("Babe", "Ruth")
aaron.info <- getinfo("Hank", "Aaron")
bonds.info <- getinfo("Barry", "Bonds")
arod.info <- getinfo("Alex", "Rodriguez")

# Create a dataframe of batting with only those four
batting <- read.csv("Batting.csv")
ruth.data <- subset(batting, playerID == ruth.info$name.code)
ruth.data$age <- ruth.data$yearID - ruth.info$byear
aaron.data <- subset(batting, playerID == aaron.info$name.code)
aaron.data$age <- aaron.data$yearID - aaron.info$byear
bonds.data <- subset(batting, playerID == bonds.info$name.code)
bonds.data$age <- bonds.data$yearID - bonds.info$byear
arod.data <- subset(batting, playerID == arod.info$name.code)
arod.data$age <- arod.data$yearID - arod.info$byear

# plot cumulative sum of home runs. type='l' is line plot. lty is line type
# lwd is line width
with(ruth.data, plot(age, cumsum(HR), type='l', lty=3, lwd=2, xlab="Age", 
                     ylab="Career Home Runs", xlim=c(18, 45), ylim=c(0, 800)))
with(aaron.data, lines(age, cumsum(HR), type='l', lty=2, lwd=2))
with(bonds.data, lines(age, cumsum(HR), type='l', lty=1, lwd=2))
with(arod.data, lines(age, cumsum(HR), type='l', lty=4, lwd=2))
legend(20, 700, legend=c("Bonds", "Aaron", "Ruth", "Arod"), lty=1:4, lwd=2)










