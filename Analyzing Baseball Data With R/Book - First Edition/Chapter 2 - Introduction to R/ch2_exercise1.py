import numpy as np
import matplotlib.pyplot as plt
# The following table gives the number of stolen bases (SB), the number of
# times caught stealing (CS), and the number of games played (G) for nine
# players currently inducted in the hall of fame

# (a) 
# In R, place the stolen base, caught stealing, and game counts in the
# vectors SB, CS, and G
SB = np.array([1406, 938, 897, 741, 738, 689, 606, 504, 474])
CS = np.array([335, 307, 212, 195, 109, 162, 136, 131, 114])
G = np.array([3081, 2616, 3034, 2826, 2476, 2649, 2599, 2683, 2379])

# (b)
# For all players compute the number of stolen base attempts SB + CS and store
# in SB.Attempt
SB_Attempt = SB + CS

# (c)
# For all players, compute the success rate Success.Rate = SB / SB.Attempt
Success_Rate = SB / SB_Attempt

# (d) 
# Compute the number of stolen bases per game SB.Game = SB / Game
SB_Game = SB / G

# (e)
# Construct a scatterplot of the stolen bases per game against the success rates
# Are the particular players with unusually high or low stolen base success
# rates? Which player had the greateest number of stolen bases per game
plt.scatter(SB_Game, Success_Rate)

# Max Carey had an unusually high success rate
# Ricky Henderson had the highest rate of stolen bases per game