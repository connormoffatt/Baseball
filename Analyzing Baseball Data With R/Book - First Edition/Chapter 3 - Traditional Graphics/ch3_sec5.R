rm(list=ls())

# Numeric Variable: Stripchart and Histogram
# Stripchart is just a one dimensional scatterplot

chapter_path = "C:/Users/conno/Documents/GitHub/Baseball/Analyzing Baseball Data With R/Book - First Edition/Chapter 3 - Traditional Graphics"
setwd(chapter_path)

# read in hall of fame batting
hof <- read.csv("hofbatting.csv")

# Create new variable era using cut function on dataframe
hof$MidCareer <- with(hof, (From + To) / 2)

# Create new window 7 inches wide and 3.5 tall
windows(width=7, height=3.5)

# Create stripchart. pch is the marker type. jitter spreads out slightly
stripchart(hof$MidCareer, method="jitter", pch=1, xlab="Mid Career")

# Create histogram for midcareer
hist(hof$MidCareer, xlab="Mid Career", main="")

# Create histogram with specific breaks
hist(hof$MidCareer, xlab="Mid Career", main="", 
     breaks=seq(1880, 2000, by=20))

