rm(list=ls())

# (a)
# Read the Lahman "pitching.csv" data file into R into a dataframe Pitching
chapter_path = "C:/Users/conno/Documents/GitHub/Baseball/Analyzing Baseball Data With R/Book - First Edition/Chapter 2 - Introduction to R"
setwd(chapter_path)
Pitching <- read.csv("pitching.csv")

# (b)
# The following function computes the comulative strikeouts, cumulative walks,
# mid career year, and total innings pitched (in terms of outs) for a pitcher
# whose season statistics are stored in the datafrme d

stats <- function(d){
  c.SO <- sum(d$SO, na.rn=TRUE)
  c.BB <- sum(d$BB, na.rn=TRUE)
  c.IPouts <- sum(d$IPouts, na.rn=TRUE)
  c.midYear <- median(d$yearID, na.rn=TRUE)
  data.frame(SO=c.SO, BB=c.BB, IPouts=c.IPouts, midYear=c.midYear)
}

# Using the funciton ddply together with the function stats, find the career
# statistics for all pitchers in the pitching dataset. Call this new data
# frame career.pitching
career.pitching <- ddply(Pitching, .(playerID), stats)

# (c)
# Use the merge function to merge the Pitching and career.pitching data frames
Pitching <- merge(Pitching, career.pitching, by="playerID")

# (d)
# Use the subset function to construct a new data frame career.10000
# consisting of data for only those pitchers with at least 10,000 career
# IPouts
career.10000 <- subset(career.pitching, career.pitching$IPouts >= 10000)

# (e)
# For the pitchers with at least 10,000 career IPouts, construct a scatterplot
# of mid career year and ratio of strikeouts to walks. Comment on the general
# pattern in this scatterplot
career.10000$SO.BB.Ratio <- career.10000$SO / career.10000$BB
plot(career.10000$midYear, career.10000$SO.BB.Ratio)

# The strikeout to walk ratio increases over time as Mid Year increases
