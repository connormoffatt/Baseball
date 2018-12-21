import pandas as pd
import matplotlib.pyplot as plt
# Pythagorean Residuals for Poor and Great Teams in the 19th Century

# As baseball was evolving into its ultimate form, nineteenth century leagues
# often featured abysmal teams that did not even succeed in finishing their
# season, as well as some dominant clubs

# (a)
# Fit a Pythagorean formula model to the run-differential, win-loss data for
# teams who played in the 19th century.
teams = pd.read_csv("Teams.csv")

# Create data frame with a reduced number of attributes
keep = ["teamID", "yearID", "lgID", "G", "W", "L", "R", "RA"]
myteams = teams[(teams.yearID >= 1800) & (teams.yearID <= 1899)].loc[:, 
                    keep]

# Calculate pythagorean win percentage
myteams['pytWpct'] = myteams.R**2 / (myteams.R**2 + myteams.RA**2)

# (b)
# By inspecting the residual plot of your fitted model form (a), did the great
# and poor eams in the 19th century do better or worse than one would expect
# on the basis of their run differentials

# Calculate run differential and winning percentage
myteams['RD'] = myteams.R - myteams.RA
myteams['Wpct'] = myteams.W / (myteams.W + myteams.L)

# Calculate residuals of pytWpct
myteams['pytResiduals'] = myteams.Wpct - myteams.pytWpct

fig, ax = plt.subplots()
scatter1 = plt.scatter(myteams.RD, myteams.pytResiduals)
ax.set(title='Pythagorean Win Residuals During 19th Century', 
       xlabel= 'Run Differential', ylabel='Residual')

# The Pythagorean formula does not perform better or worse than expected for 
# teams that are abysmal or dominant
