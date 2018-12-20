rm(list=ls())

# The variable WAR is the total wins above replacement of the pitcher during
# his career

# (a)
# Using the hist function, construct a histogram of WAR foor the pitchers in the
# Hall of Fame dataset
hofpitching <- read.csv("hofpitching.csv")
hist(hofpitching$WAR, xlab="WAR", main="Distribution of WAR", xlim=c(0,200))

# (b)
# There are two pitchers who stand out among all of the Hall of Famers on the
# total WAR variable. Identify these two pitchers
hofpitching <- hofpitching[order(hofpitching$WAR),]
tail(hofpitching)

# The top two pitchers in WAR are Walter Johnson and Cy Young