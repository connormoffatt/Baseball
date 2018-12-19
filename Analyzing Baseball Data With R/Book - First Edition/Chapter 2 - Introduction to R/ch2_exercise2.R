rm(list=ls())

# Suppose one records the outcome of a batter in ten plate appearances:
# Single, Out, Out, Single, Out, Double, OUt, Walk, Out, Single

# (a)
# use the c function to collect these outcomes into a character vector
outcomes <- c("Single", "Out", "Out", "Single", "Out", "Double", "Out",
              "Walk", "Out", "Single")

# (b)
# Use the table funciton to construct a frequency table of outcomes
table(outcomes)

# (c)
# In tabulating these results, suppose one prefers the results to be ordered
# from least-successful to most-successful. Use the following code to convert
# the character vector outcomes to a factor variable f.outcomes
# f.outcomes <- factor(outcomes, levels=("Out", "Walk", "Single", "Double"))
# Use the table function to tabulate the values of f.outcomes. How does the
# output differ from what you saw in part(b)
f.outcomes <- factor(outcomes, levels=c("Out", "Walk", "Single", "Double"))
table(f.outcomes)
# The table is now ordered by the levels that we have set 

# (d)
# Suppose you want to focus only on the walks in the plate appearances. Describe
# waht is done in each of the following statements

outcomes == "Walk"
# provides boolean values of true and false dependent on if the batter walked

sum(outcomes == "Walk")
# provides a count of how many times the batter walked