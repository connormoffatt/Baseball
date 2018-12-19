import numpy as np
import pandas as pd
# The following table lists nine ptichers who have 350 career wins

# (a)
# In R, place the wins and losses in the vector W and L, respectively. Also,
# create a character vector name containing the last names of these ptichers
W =  np.array([373, 354, 364, 417, 355, 373, 361, 363, 511])
L =  np.array([208, 184, 310, 279, 227, 188, 208, 245, 316])
Name =  ["Alexander", "Clemens", "Galvin", "Johnson", "Maddux", "Mathewson", 
           "Nichols", "Spahn", "Young"]

# (b)
# Compute the winning percentage for all pitchers defined by 100 x W / (W + L)
# and put these winning percentages in the vector Win.PCT
Win_PCT = W / (W + L)

# (c)
# By use of the command Wins.350 = data.frame(Name, W, L, Win.PCT) create a
# dataframe Wins.350 containing the names, wins, losses, and winning %
Wins_350 = pd.DataFrame()
Wins_350['Name'] = Name
Wins_350['W'] = W
Wins_350['L'] = L
Wins_350['Win_PCT'] = Win_PCT

# (d)
# By use of the order function to sort the data from Wins.350 by winningn %.
# Among these pitchers who had the largest and smallest winning percentage
Wins_350 = Wins_350.sort_values('Win_PCT')

