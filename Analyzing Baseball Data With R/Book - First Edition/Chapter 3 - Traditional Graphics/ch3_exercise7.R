rm(list=ls())

# In Section 3.9, we used the Retrosheet play-by-play data to explore the home
# run race between mark McGwire and Sammy Sosa in the 1998 season. Another way
# to compare the patterns of home run hitting of the two players i sto 
# compute the spacings, the number of plate appearnces between homme runs

# (a)
# Following the work of Section 3.9, create two data frames mac.data and
# sosa.data containing the batting  data for the two players
chapter_path = "C:/Users/conno/Documents/GitHub/Baseball/Analyzing Baseball Data With R/Book - First Edition/Chapter 3 - Traditional Graphics"
setwd(chapter_path)

# read in 1998 play by play data and headers
data.1998 <- read.csv("all1998.csv", header=FALSE)
fields <- read.csv("fields.csv")

# Change column names in R
names(data.1998) <-  fields[,"Header"]

# Find the id for Sosa and McGwire. id's for retrosheet are in retrosheetIDs
retro.ids <- read.csv("retrosheetIDs.csv")
sosa.id <- as.character(subset(retro.ids, FIRST=="Sammy" & LAST=="Sosa")$ID)
mac.id <- as.character(subset(retro.ids, FIRST=="Mark" & LAST=="McGwire")$ID)

# Create player dataframes for every event when they were the batter
sosa.data <- subset(data.1998, BAT_ID==sosa.id)
mac.data <- subset(data.1998, BAT_ID==mac.id)

# (b)
# Use the following R commands to restrict the two data frames to the plays
# where a batting event occurred
mac.data <- subset(mac.data, BAT_EVENT_FL == TRUE)
sosa.data <- subset(sosa.data, BAT_EVENT_FL == TRUE)

# (c)
# For each data frame, create a new variable PA that numbers the plate
# appearances 1, 2, ... (The function nrow gives the number of rows of a
# data frame)
mac.data$PA <- 1:nrow(mac.data)
sosa.data$PA <- 1:nrow(sosa.data)

# (d)
# The following commands will return the numbers of the plate appearances when
# the players hit home runs
mac.HR.PA <- mac.data$PA[mac.data$EVENT_CD==23]
sosa.HR.PA <- mac.data$PA[sosa.data$EVENT_CD==23]

# (e)
# Using the R function diff, the following commands compute the spacings 
# between the occurrences of home runs
mac.spacings <- diff(c(0, mac.HR.PA))
sosa.spacings <- diff(c(0, sosa.HR.PA))

# (f)
# By use of the summary and hist functions on the vectors mac.spacings and
# sosa.spacings, compare the home run spacings of the two players
#hist(mac.spacing)

#hist(hof$MidCareer, xlab="Mid Career", main="")
summary(mac.spacings)
summary(sosa.spacings)
hist(mac.spacings, xlab="PA between HR", main="Mark McGwire HR Spacing")
hist(sosa.spacings, xlab="PA between HR", main="Sammy Sosa HR Spacing")

# We see that Mark McGwire Hit had less spacing than Sammy Sosa. Also, we notice
# however, that Sosa's has a large spacing near 50 plate appearances
