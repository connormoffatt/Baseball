import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# To understand a pitcher's season contribution, suppose we define the new
# variable WAR.Season defined by
hofpitching = pd.read_csv("./hofpitching.csv")
hofpitching['WAR_Season'] = hofpitching['WAR'] / hofpitching['Yrs']

# The variable BF is the number of batters faced by a pitcher in his career
# suppose we group the pitchers by this variable using the intervals
# (0, 10,000), (10,000, 15,000), (15,000, 20,000), (20,000, 30,000). One can
# reexpress the variable BF to the grouped variable BF.group by use of the cut
# function

group_breaks = np.array([0, 10000, 15000, 20000, 30000])
group_labels = ["Less than 10000", "(10000, 15000)", "(15000, 20000)",
                 "More than 20000"]

hofpitching['BF_group'] = pd.cut(hofpitching['BF'], bins=group_breaks,
           labels=group_labels)

# (a)
# Use the stripchart function to construct parallel stripcharts of WAR.Season
# for the different levels of BP.group
# Default sizes in the following order: bot, left, top, right
fig, ax = plt.subplots()
strip1 = sns.stripplot(x=hofpitching['WAR_Season'], y=hofpitching['BF_group'],
                       jitter=1, orient='h')
ax.set(title='WAR Per Season by Batters Faced')

# (b)
# Use the boxplot function to construct parallel boxplots of WAR.Season across
# BP.group
fig, ax = plt.subplots()
box1 = sns.boxplot(x=hofpitching['WAR_Season'], y=hofpitching['BF_group'])
ax.set(title='WAR Per Season by Batters Faced')

# (c)
# Based on your graphs, how does the wins above replacement per season depend
# on the number of batters faced

# WAR increases with batters faced because WAR is a cumulative statistic