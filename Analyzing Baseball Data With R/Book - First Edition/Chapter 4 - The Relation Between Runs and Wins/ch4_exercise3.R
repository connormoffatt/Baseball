rm(list=ls())

# Exploring the Manager Effect in Baseball

# Retrosheet game logs report, for every game played, the managers of both teams

# (a)
# Select a period of your choice (encompassing at least ten years) and
# fit the Pythagorean formula model to the run-differential, win-loss data

# Fit a Pythagorean formula model to the run-differential, win-loss data for
# teams who played in the 19th century.
teams <- read.csv("Teams.csv")

# Create data frame with a reduced number of attributes
keep_col = c("teamID", "yearID", "lgID", "G", "W", "L", "R", "RA")
myteams <- subset(teams, yearID >= 2000 & yearID <= 2009)[, keep_col]

# Calculate pythagorean win percentage
myteams$pytWpct <- with(myteams, R^2 / (R^2 + RA^2))

# (b)
# On the basis of your fit in part (a) and the list of managers, compile a list
# of the managers who most overperformed their Pythagorean winning percentage
# and the managers who most overperformed it

# For simplicity we will simply find the top 5 teams that overperformed and
# underperformed and search for the managers online
myteams$Wpct = with(myteams, W / (W + L))
myteams$pytResiduals <- myteams$Wpct - myteams$pytWpct
myteams <- myteams[order(myteams$pytResiduals), ]

head(myteams)
tail(myteams)

# The 5 most overperforming teams are 
# Cleveland 2006: Eric Wedge
# Colorado 2001: Buddy Bell
# Toronto 2009: Cito Gaston
# Toronto 2005: John Gibbons
# Houston 2000: Larry Dierker

# The 5 most underperforming teams are
# Cincinnati 2004: Dave Miley
# Seattle 2009: Don Wakamatsu
# Arizona 2007: Bob Melvin
# Angels 2008: Mike Scioscia
# Yankees 2004: Joe Torre