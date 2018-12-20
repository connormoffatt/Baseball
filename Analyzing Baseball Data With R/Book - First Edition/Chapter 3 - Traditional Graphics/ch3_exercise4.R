rm(list=ls())

# Suppose we limit our exploration to pitchers whose mid-career was 1960 or
# later. We define the MidYear variable and then use the subset function to
# construct a data frmae consisting of only these 1960+ pitchers

hofpitching <- read.csv("hofpitching.csv")
hofpitching$WAR.Season <- with(hofpitching, WAR / Yrs)
hofpitching$MidYear <- with(hofpitching, (From + To) / 2)
hofpitching.recent <- subset(hofpitching, MidYear >= 1960)

# (a)
# By use of the order funciton, order the rows of the data frame by the value
# of WAR.Season
hofpitching.recent <- hofpitching.recent[order(hofpitching.recent$WAR.Season),]

# (b)
# Construct a dot plot of the values of WAR.Season where the labels are the 
# pitcher names

dotchart(hofpitching.recent$WAR.Season, labels=hofpitching.recent$X,
         xlab="WAR per Season", cex.lab=1, cex.axis=0.75,
         main="War Per Season By Pitcher")

# (c)
# Which two 1960+ pitchers stand out with respect to wins above replacement
# per season

# The two pitchers that stand out are Tom Seaver and Bob Gibson