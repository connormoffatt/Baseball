import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# Suppose we limit our exploration to pitchers whose mid-career was 1960 or
# later. We define the MidYear variable and then use the subset function to
# construct a data frmae consisting of only these 1960+ pitchers

hofpitching = pd.read_csv("hofpitching.csv")
hofpitching['WAR_Season'] = hofpitching['WAR'] / hofpitching['Yrs']
hofpitching['MidYear'] = (hofpitching['From'] + hofpitching['To']) / 2
hofpitching_recent = hofpitching[hofpitching['MidYear'] >= 1960]

# (a)
# By use of the order funciton, order the rows of the data frame by the value
# of WAR.Season
hofpitching_recent = hofpitching_recent.sort_values(by=['WAR_Season'], 
                                                    ascending=False)

# (b)
# Construct a dot plot of the values of WAR.Season where the labels are the 
# pitcher names

fig, ax = plt.subplots()
dot1 = sns.pointplot(x=hofpitching_recent['WAR_Season'],
                        y=hofpitching_recent['Unnamed: 1'],
                        linestyles='')
ax.set(title='WAR Per Season by Pitcher', ylabel='Pitcher',
       xlabel='Average WAR per Season')

# (c)
# Which two 1960+ pitchers stand out with respect to wins above replacement
# per season

# The two pitchers that stand out are Tom Seaver and Bob Gibson