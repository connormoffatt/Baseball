import numpy as np
import pandas as pd

# (a)
# In R, place the strikeout and walk totals from the 350 win pitchers in the
# vectors SO and BB respectively. Also, create a character vector Name 
# containing the names of these pitchers
SO = np.array([2198, 4672, 1806, 3509, 3371, 2502, 1868, 2583, 2803])
BB = np.array([951, 1580, 745, 1363, 999, 844, 1268, 1434, 1217])
Name =  ["Alexander", "Clemens", "Galvin", "Johnson", "Maddux", "Mathewson", 
           "Nichols", "Spahn", "Young"]

# (b)
# Compute the strikeout-walk ratio by SO/BB and put these ratios in the
# vector SO.BB.Ratio
SO_BB_Ratio = SO / BB

# (c)
# By use of the command SO.BB = data.frame(Name, SO, BB, SO.BB.Ratio)
# create a dataframe SO.BB containing the names, strikeouts, walks, ratios
SO_BB = pd.DataFrame()
SO_BB['Name'] = Name
SO_BB['SO'] = SO
SO_BB['BB'] = BB
SO_BB['SO_BB_Ratio'] = SO_BB_Ratio


# (d)
# By use of the subset function, find the pitchers who had a strikeout walk
# ratio exceeding 2.8
SO_BB_28 =  SO_BB[SO_BB['SO_BB_Ratio'] > 2.8]

# (e)
# By use of the order function, sort hte data frame by the number of walks.
# Did the pitcher with the largest n umber of walks have a high or low K/BB
# ratio
SO_BB = SO_BB.sort_values('SO_BB_Ratio')

# Clemens had the highest number of walks but still had a high strikeout to
# walk ratio. This is because he had significantly more strikeouts than anyone
# else