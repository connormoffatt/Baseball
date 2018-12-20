rm(list=ls())

# The variables MidYear and WAR.Season are defined in the previous exercises
hofpitching <- read.csv("hofpitching.csv")
hofpitching$WAR.Season <- with(hofpitching, WAR / Yrs)
hofpitching$MidYear <- with(hofpitching, (From + To) / 2)

# (a)
# Construct a scatterplot of MidYear (horizontal) against WAR.Season (vertical)
with(hofpitching, plot(MidYear, WAR.Season, 
                       main="Pitcher Mid Career Year v. War per Season"))

# (b)
# Is there a general pattern in this scatterplot? Explain.

# It appears that WAR per season tends to decrease as mid career year increases
# but the trend is not strong

# (c)
# There are two pitchers whose mid careers were in the 1800s who had relatively
# low WAR.Season values. Use the identify function with the scatterplot
# to find the names of these two pitchers

with(hofpitching, identify(MidYear, WAR.Season, X, n=2, cex=0.75))
#  The two pitchers are Al Spalding and Candy Cummings