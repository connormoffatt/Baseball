import numpy as np
from itertools import groupby

# Suppose one records the outcome of a batter in ten plate appearances:
# Single, Out, Out, Single, Out, Double, OUt, Walk, Out, Single

# (a)
# use the c function to collect these outcomes into a character vector
outcomes = ["Single", "Out", "Out", "Single", "Out", "Double", "Out",
              "Walk", "Out", "Single"]
outcomes2 = outcomes.copy()

# (b)
# Create a frequency dictionary from the outcomes
outcomes.sort()
freq = [len(list(g)) for key, g in groupby(outcomes)]
freq_dict = dict(zip(set(outcomes),freq))

# (c)
# In tabulating these results, suppose one prefers the results to be ordered
# from least-successful to most-successful. Use the following code to convert
# the character vector outcomes to a factor variable f.outcomes
# f.outcomes <- factor(outcomes, levels=("Out", "Walk", "Single", "Double"))
# Use the table function to tabulate the values of f.outcomes. How does the
# output differ from what you saw in part(b)

# UNNECESSARY FOR PYTHON

# The table is now ordered by the levels that we have set 

# (d)
# Suppose you want to focus only on the walks in the plate appearances. Describe
# what is done in each of the following statements
walk = [e == "Walk" for e in outcomes2]
# provides boolean values of true and false dependent on if the batter walked

np.sum(walk)
# provides a count of how many times the batter walked