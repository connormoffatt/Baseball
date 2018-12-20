rm(list=ls())

# A Numberic Variable and a Factor Variable

chapter_path = "C:/Users/conno/Documents/GitHub/Baseball/Analyzing Baseball Data With R/Book - First Edition/Chapter 3 - Traditional Graphics"
setwd(chapter_path)

# read in hall of fame batting
hof <- read.csv("hofbatting.csv")

# Create a variable to get the home run rate
hof$HR.rate <- with(hof, HR / AB)

# Create new variable era using cut function on dataframe
hof$MidCareer <- with(hof, (From + To) / 2)
era_years = c(1800, 1900, 1919, 1941, 1960, 1976, 1993, 2050)
era_names = c("19th Century", "Dead Ball", "Lively Ball", "Integration",
              "Expansion", "Free Agency", "Long Ball")
hof$Era <- cut(hof$MidCareer, breaks=era_years, labels=era_names)

# create a parallel stripchart
stripchart(HR.rate ~ Era, data=hof)

# stripchart with everything cleaned
stripchart(HR.rate ~ Era, data=hof, las=2, pch=1, method='jitter')

# create a parallel boxplot. Error with plot region too large in RStudio
#png("boxplot.png")
par(plt=c(.2, .94, .145, 883))
boxplot(HR.rate ~ Era, data=hof, las=2, horizontal=TRUE, xlab="Home Run Rate")
#dev.off()
