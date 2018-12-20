rm(list=ls())

# Dot Plots

chapter_path = "C:/Users/conno/Documents/GitHub/Baseball/Analyzing Baseball Data With R/Book - First Edition/Chapter 3 - Traditional Graphics"
setwd(chapter_path)

# read in hall of fame batting
hof <- read.csv("hofbatting.csv")

# Create new variable era using cut function on dataframe
hof$MidCareer <- with(hof, (From + To) / 2)
era_years = c(1800, 1900, 1919, 1941, 1960, 1976, 1993, 2050)
era_names = c("19th Century", "Dead Ball", "Lively Ball", "Integration",
              "Expansion", "Free Agency", "Long Ball")
hof$Era <- cut(hof$MidCareer, breaks=era_years, labels=era_names)

T.era <- table(hof$Era)

# Create dotchart with era names being the labels on the y axis
dotchart(as.numeric(T.era), labels=era_names, xlab="Frequency")

# Create dataframe of HOF players with at least 500 HR and sort by OPS
hof.500 <- subset(hof, HR >=500)
hof.500 <- hof.500[order(hof.500$OPS),]

# Dot chart of OPS for HOF players with at least 500 HR
dotchart(hof.500$OPS, labels=hof.500$X, xlab="OPS")

