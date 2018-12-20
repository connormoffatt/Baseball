import pandas as pd
import matplotlib.pyplot as plt

# The data file "hofpitching.csv" contains the career pitching statistics for
# all of the pitchers inducted in the Hall of Fame. This data file can be read
# into R by means of the read.csv function

hofpitching = pd.read_csv("./hofpitching.csv")

# The variable WAR is the total wins above replacement of the pitcher during
# his career

# (a)
# Using the hist function, construct a histogram of WAR foor the pitchers in the
# Hall of Fame dataset
fig, ax = plt.subplots()
bar1 = ax.hist(hofpitching['WAR'])
ax.set(title='WAR of HOF Pitchers', xlabel='WAR', ylabel='Frequency')

# (b)
# There are two pitchers who stand out among all of the Hall of Famers on the
# total WAR variable. Identify these two pitchers
hofpitching = hofpitching.sort_values(by=['WAR'], ascending=False)
print(hofpitching.iloc[0:2, :])

# The top two pitchers in WAR are Walter Johnson and Cy Young