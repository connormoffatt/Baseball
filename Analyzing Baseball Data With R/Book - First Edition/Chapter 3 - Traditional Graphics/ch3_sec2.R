rm(list=ls())

# Factor Variable

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

# See distribution of era of hall of famers
T.era <- table(hof$Era)
barplot(T.era)

# Add title and axis labels to barplot from above
barplot(T.era, xlab="Era", ylab="# Players", main="Era of Hall of Fame Baseball
        Players")

# Vetrical linegraphs of frequencies
plot(T.era)

# pie chart of frequencies
pie(T.era)
