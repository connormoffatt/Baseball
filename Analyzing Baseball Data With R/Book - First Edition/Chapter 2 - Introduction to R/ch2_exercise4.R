rm(list=ls())

# (a)
# In R, place the strikeout and walk totals from the 350 win pitchers in the
# vectors SO and BB respectively. Also, create a character vector Name 
# containing the names of these pitchers
SO = c(2198, 4672, 1806, 3509, 3371, 2502, 1868, 2583, 2803)
BB = c(951, 1580, 745, 1363, 999, 844, 1268, 1434, 1217)
Name <-  c("Alexander", "Clemens", "Galvin", "Johnson", "Maddux", "Mathewson", 
           "Nichols", "Spahn", "Young")

# (b)
# Compute the strikeout-walk ratio by SO/BB and put these ratios in the
# vector SO.BB.Ratio
SO.BB.Ratio = SO / BB

# (c)
# By use of the command SO.BB <- data.frame(Name, SO, BB, SO.BB.Ratio)
# create a dataframe SO.BB containing the names, strikeouts, walks, ratios
SO.BB <- data.frame(Name, SO, BB, SO.BB.Ratio)

# (d)
# By use of the subset function, find the pitchers who had a strikeout walk
# ratio exceeding 2.8
subset(SO.BB, SO.BB$SO.BB.Ratio > 2.8)

# (e)
# By use of the order function, sort hte data frame by the number of walks.
# Did the pitcher with the largest n umber of walks have a high or low K/BB
# ratio
pos <- order(SO.BB$BB)
SO.BB <- SO.BB[pos,]

# Clemens had the highest number of walks but still had a high strikeout to
# walk ratio. This is because he had significantly more strikeouts than anyone
# else