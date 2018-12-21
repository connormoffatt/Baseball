import pandas as pd
from sklearn import linear_model
import numpy as np
# Section 4.3 used a simple linear model to predict a team's winning percentage
# based on its run differential. This model was fit using team data since the
# 2001 season

# (a)
# refit this linear model using data from the seasons 1961-1970, 1971-1980,
# 1981-1990, 1991-2000

# load in teams table and display the last 5 rows with tail
teams = pd.read_csv("Teams.csv")

# Create data frame with a reduced number of attributes
keep = ["teamID", "yearID", "lgID", "G", "W", "L", "R", "RA"]
myteams1960 = teams[(teams.yearID >= 1961) & (teams.yearID <= 1970)].loc[:, 
                    keep]
myteams1970 = teams[(teams.yearID >= 1971) & (teams.yearID <= 1980)].loc[:, 
                    keep]
myteams1980 = teams[(teams.yearID >= 1981) & (teams.yearID <= 1990)].loc[:, 
                    keep]
myteams1990 = teams[(teams.yearID >= 1991) & (teams.yearID <= 2000)].loc[:, 
                    keep]

# Calculate run differential and winning percentage
myteams1960['RD'] = myteams1960.R - myteams1960.RA
myteams1960['Wpct'] = myteams1960.W / (myteams1960.W + myteams1960.L)

myteams1970['RD'] = myteams1970.R - myteams1970.RA
myteams1970['Wpct'] = myteams1970.W / (myteams1970.W + myteams1970.L)

myteams1980['RD'] = myteams1980.R - myteams1980.RA
myteams1980['Wpct'] = myteams1980.W / (myteams1980.W + myteams1980.L)

myteams1990['RD'] = myteams1990.R - myteams1990.RA
myteams1990['Wpct'] = myteams1990.W / (myteams1990.W + myteams1990.L)

# Create linear regression objects
regr1960 = linear_model.LinearRegression()
regr1970 = linear_model.LinearRegression()
regr1980 = linear_model.LinearRegression()
regr1990 = linear_model.LinearRegression()

# Data needs to be placed into a 2D numpy array to perform regression
# Get coefficients and intercepts through the methods .coef_ and .intercept_
regr1960.fit(np.array(myteams1960.RD)[:, np.newaxis], 
             np.array(myteams1960.Wpct))
regr1970.fit(np.array(myteams1970.RD)[:, np.newaxis], 
             np.array(myteams1970.Wpct))
regr1980.fit(np.array(myteams1980.RD)[:, np.newaxis], 
             np.array(myteams1980.Wpct))
regr1990.fit(np.array(myteams1990.RD)[:, np.newaxis], 
             np.array(myteams1990.Wpct))

# (b)
# Compare across the five decades the predicted winning percentage for a team
# with a run differential of 10 runs

tenwin = np.array([10])[:, np.newaxis]
print('1960: ' + str(regr1960.predict(tenwin)[0]))
print('1970: ' + str(regr1970.predict(tenwin)[0]))
print('1980: ' + str(regr1980.predict(tenwin)[0]))
print('1990: ' + str(regr1990.predict(tenwin)[0]))

