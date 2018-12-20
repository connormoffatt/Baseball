rm(list=ls())

# To understand a pitcher's season contribution, suppose we define the new
# variable WAR.Season defined by
hofpitching <- read.csv("hofpitching.csv")
hofpitching$WAR.Season <- with(hofpitching, WAR / Yrs)

group_breaks = c(0, 10000, 15000, 20000, 30000)
group_labels = c("Less than 10000", "(10000, 15000)", "(15000, 20000)",
                 "more than 20000")
hofpitching$BF.group <- with(hofpitching, cut(BF, group_breaks, 
                                              labels=group_labels))

# (a)
# Use the stripchart function to construct parallel stripcharts of WAR.Season
# for the different levels of BP.group
# Default sizes in the following order: bot, left, top, right
par(mar=c(6, 6, 6, 3))
stripchart(WAR.Season ~ BF.group, data=hofpitching, las=1, pch=1, 
           method='jitter', main="War Per Season by Batters Faced",
           cex.lab=1, cex.axis=0.75)

# (b)
# Use the boxplot function to construct parallel boxplots of WAR.Season across
# BP.group
par(mar=c(6, 6, 6, 3))
boxplot(WAR.Season ~ BF.group, data=hofpitching, las=1, horizontal=TRUE,
        xlab="WAR", cex.axis=0.75, 
        main="Box Plot of War per Season by Batters Faced")

# (c)
# Based on your graphs, how does the wins above replacement per season depend
# on the number of batters faced

# WAR increases with batters faced because WAR is a cumulative statistic