rm(list=ls())

# Saving Graphs

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

# Can save plot through the RStudio Plots Viewer

# Can also save a plot as follows 
png("bargraph.png")
barplot(T.era, xlab="Era", ylab="# Players", main="Era of Hall of Fame Baseball
        Players")
# dev.off means that no graph will be displayed
dev.off()

# Can save multiple plots to a pdf
pdf("graphs.pdf")
barplot(T.era, xlab="Era", ylab="# Players", main="Era of Hall of Fame Baseball
        Players")
plot(table(hof$Era))
# dev.off means that no graph will be displayed
dev.off()
