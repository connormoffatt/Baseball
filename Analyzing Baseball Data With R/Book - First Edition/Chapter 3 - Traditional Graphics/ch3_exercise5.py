import pandas as pd
import matplotlib.pyplot as plt

# The variables MidYear and WAR.Season are defined in the previous exercises
hofpitching = pd.read_csv("hofpitching.csv")
hofpitching['WAR_Season'] = hofpitching['WAR'] / hofpitching['Yrs']
hofpitching['MidYear'] = (hofpitching['From'] + hofpitching['To']) / 2
hofpitching_recent = hofpitching[hofpitching['MidYear'] >= 1960]

# (a)
# Construct a scatterplot of MidYear (horizontal) against WAR.Season (vertical)
fig, ax = plt.subplots()
scatter1 = plt.scatter(hofpitching['MidYear'], hofpitching['WAR_Season'])
ax.set(title='War Per Season v. Career MidYear', xlabel='Career Midyear',
       ylabel='War Per Season')

# (b)
# Is there a general pattern in this scatterplot? Explain.

# It appears that WAR per season tends to decrease as mid career year increases
# but the trend is not strong

# (c)
# There are two pitchers whose mid careers were in the 1800s who had relatively
# low WAR.Season values. Use the identify function with the scatterplot
# to find the names of these two pitchers

# NOTE: could not find an equivalent function as identify in Python

# The two pitchers are Al Spalding and Candy Cummings