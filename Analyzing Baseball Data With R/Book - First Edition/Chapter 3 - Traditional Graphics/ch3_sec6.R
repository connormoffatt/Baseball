rm(list=ls())

# Two Numeric Variables

chapter_path = "C:/Users/conno/Documents/GitHub/Baseball/Analyzing Baseball Data With R/Book - First Edition/Chapter 3 - Traditional Graphics"
setwd(chapter_path)

# read in hall of fame batting
hof <- read.csv("hofbatting.csv")

# Create new variable era using cut function on dataframe
hof$MidCareer <- with(hof, (From + To) / 2)

# Scatter plot of MidCareer and OPS with a smoothing curve and identify will
# provide text of which person when clicking near the point

# Using identify: it will wait for you to click n times on the plot and label
# the closest point. Location of click will determine location of text
# relative to thte point. Selection must be within 0.25 inches of point
with(hof, plot(MidCareer, OPS))
with(hof, lines(lowess(MidCareer, OPS, f=0.3)))
with(hof, identify(MidCareer, OPS, X, n=4))

# scatterplot of obp andn slg
with(hof, plot(OBP, SLG))

# better limits, labels, and markers to the scatterplot
with(hof, plot(OBP, SLG, xlim=c(0.25,0.5), ylim=c(0.28,0.75),
               xlab="On-Base Percentage", ylab="Slugging Percentage",
               pch=19))

# add ops curves and ops text labels
curve(0.7 - x, add=TRUE)
curve(0.8 - x, add=TRUE)
curve(0.9 - x, add=TRUE)
curve(1.0 - x, add=TRUE)
text(0.27, 0.42, "OPS=0.7")
text(0.27, 0.52, "OPS=0.8")
text(0.27, 0.62, "OPS=0.9")
text(0.27, 0.72, "OPS=1.0")

# We can use identify to label the top 6 
# with(hof, identify(OBP, SLG, X, n=6))
      
      
      
      
      
