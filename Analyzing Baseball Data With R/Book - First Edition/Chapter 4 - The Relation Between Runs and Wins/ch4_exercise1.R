rm(list=ls())

# Section 4.3 used a simple linear model to predict a team's winning percentage
# based on its run differential. This model was fit using team data since the
# 2001 season

# (a)
# refit this linear model using data from the seasons 1961-1970, 1971-1980,
# 1981-1990, 1991-2000

# load in teams table and display the last 5 rows with tail
teams <- read.csv("Teams.csv")

# Create data frame with a reduced number of attributes
keep_col = c("teamID", "yearID", "lgID", "G", "W", "L", "R", "RA")
myteams1960 <- subset(teams, yearID >= 1961 & yearID <= 1970)[, keep_col]
myteams1970 <- subset(teams, yearID >= 1971 & yearID <= 1980)[, keep_col]
myteams1980 <- subset(teams, yearID >= 1981 & yearID <= 1990)[, keep_col]
myteams1990 <- subset(teams, yearID >= 1991 & yearID <= 2000)[, keep_col]
myteams2000 <- subset(teams, yearID >= 2001 & yearID <= 2010)[, keep_col]

# Calculate run differential and winning percentage
myteams1960$RD = with(myteams1960, R - RA)
myteams1960$Wpct = with(myteams1960, W / (W + L))

myteams1970$RD = with(myteams1970, R - RA)
myteams1970$Wpct = with(myteams1970, W / (W + L))

myteams1980$RD = with(myteams1980, R - RA)
myteams1980$Wpct = with(myteams1980, W / (W + L))

myteams1990$RD = with(myteams1990, R - RA)
myteams1990$Wpct = with(myteams1990, W / (W + L))

myteams2000$RD = with(myteams2000, R - RA)
myteams2000$Wpct = with(myteams2000, W / (W + L))

# Calculate the linear regression between run differential and win %
linfit1960 <- lm(Wpct ~ RD, data=myteams1960)
linfit1970 <- lm(Wpct ~ RD, data=myteams1970)
linfit1980 <- lm(Wpct ~ RD, data=myteams1980)
linfit1990 <- lm(Wpct ~ RD, data=myteams1990)
linfit2000 <- lm(Wpct ~ RD, data=myteams2000)

# (b)
# Compare across the five decades the predicted winning percentage for a team
# with a run differential of 10 runs

predict1960 <- linfit1960$coefficients[[1]] + linfit1960$coefficients*10

# Create dataframe of a team with ten predictions
tenwin <- data.frame("RD"=10)

# Create predictions
tenwin$sixties <- predict(linfit1960, tenwin)
tenwin$seventies <- predict(linfit1970, tenwin)
tenwin$eighties <- predict(linfit1980, tenwin)
tenwin$nineties <- predict(linfit1990, tenwin)
tenwin$zeros <- predict(linfit2000, tenwin)


