# Objects and Containers in R
rm(list=ls())

# Vector is a simple container with elements all of the same type

# characters (strings) are represented by letters and numbers enclosed within
# quotes

# Define world series teams, winner, number of games, and year
NL <- c("FLA", "STL", "HOU", "STL", "COL", "PHI", "PHI", "SFG", "STL", "SFG")
AL <- c("NYY", "BOS", "CHW", "DET", "BOS", "TBR", "NYY", "TEX", "TEX", "DET")
Winner <- c("NL", "AL", "AL", "NL", "NL", "NL", "AL", "NL", "NL", "NL")
N.Games <- c(6, 4, 4, 5, 4, 5, 6, 5, 7, 4)
Year <- 2003 : 2012

# A matrix is an example of a container that is not a vector
results <- matrix(c(NL, AL), 10, 2)

# dimnames can be used to add descriptions to tables
dimnames(results)[[1]] <- Year
dimnames(results)[[2]] <- c("NL Team", "AL Team")

# table will create a freq table
table(Winner)
barplot(table(Winner))

# factor is a special way to represent character data

# this table will be alphabetical
table(NL)

# if we prefer to organize by levels we can do this
NL2 <- factor(NL, levels = c("FLA", "PHI", "HOU", "STL", "COL", "SFG"))

# this will allow us to understand how the factor variables are stored
str(NL2)

# Lists can mix data types
World.Series <- list(Winner=Winner, Number.Games=N.Games, Seasons="2003 to 2012")

# To get elements of list. Can use $, index name or index number (double bracket)
# Last option returns a list rather than a vector
World.Series$Number.Games
World.Series[[2]]
World.Series["Number.Games"]
