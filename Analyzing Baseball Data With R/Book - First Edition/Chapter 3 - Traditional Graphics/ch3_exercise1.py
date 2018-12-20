import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# The data file "hofpitching.csv" contains the career pitching statistics for
# all of the pitchers inducted in the Hall of Fame. This data file can be read
# into R by means of the read.csv function

hofpitching = pd.read_csv("./hofpitching.csv")


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
# Construct a frequency table of BF.group using the table function
counts = hofpitching['BF_group'].value_counts(sort=False)

# (b)
# Construct a bar graph of the output from table. How many HOF pitchers faced
# more than 20,000 pitchers in their career?
fig, ax = plt.subplots()
bar1 = ax.bar(counts.index, counts.values)
ax.set(title='Batters Faced Group Frequency')
plt.xticks(fontsize=8)

# 14 Hall of Fame pitchers have faced more than 20,000 batters

# (c)
# Construct a pie graph of the BF.group variable. Compare the effectiveness
# of the bar graph and pie graph in comparing the frequencies in the four
# intervals

#pie(table(hofpitching$BF.group))
fig, ax = plt.subplots()
pie1 = ax.pie(counts.values, labels=counts.index)
ax.set(title='Percent Batters Faced Per Group')

# The bar chart is a lot more affective because it gives amounts rather than 
# portions






