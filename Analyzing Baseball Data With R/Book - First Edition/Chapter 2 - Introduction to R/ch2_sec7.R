rm(list=ls())

# Data frames are a fundamental object in R

# Load in spahn dataframe
# Set working directory to the current chapter
chapter_path = "C:/Users/conno/Documents/GitHub/Baseball/Analyzing Baseball Data With R/Book - First Edition/Chapter 2 - Introduction to R"
setwd(chapter_path)
spahn <- read.csv("spahn.csv")

# We can display portionso f dataframes using hte square brackets
spahn[1:3,1:10]

# blank gives all rows/columns
spahn[1,]

# Can use a container vector of strings to get attributes
spahn[1:10,c("Age", "W", "L", "ERA")]

# We can use dollar signs to get entire columns
spahn$ERA

# get age when he minimized his era
spahn$Age[spahn$ERA == min(spahn$ERA)]

# Add FIP to dataframe. with function indicates that the variables used
# are understood within the environemnet of the datframe spahn
spahn$FIP <- with(spahn, (13 * HR + 3 * BB - 2 * SO) / IP)

# head gives top of a dataframe
# gettop five years of fip
pos <- order(spahn$FIP)
head(spahn[pos, c("Year", "Age", "W", "L", "ERA", "FIP")])

# Want to split into his two teams
spahn1 <- subset(spahn, Tm=="BSN" | Tm=="MLN")
# current Tm attribute has three values BSN, MLN, TOT. Redefine so there are
# only two possible values
spahn1$Tm <- factor(spahn1$Tm, levels=c("BSN", "MLN"))

# Use "by" funcito to view statistics by team
by(spahn1[,c("W.L", "ERA", "WHIP", "FIP")], spahn1$Tm, summary)

# Suppose we want to merge two dataframes rbind (row combine)
NLbatting <- read.csv("NLbatting.csv")
ALbatting <- read.csv("ALbatting.csv")
batting <- rbind(NLbatting, ALbatting)

# merge to combine horizontally
NLpitching <- read.csv("NLpitching.csv")
NL <- merge(NLbatting, NLpitching, by="Tm")

# Create subset to see teams that hit over 150 home runs
NL.150 <- subset(NLbatting, HR > 150)


