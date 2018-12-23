rm(list=ls())

chapter_path = "C:/Users/conno/Documents/GitHub/Baseball/Analyzing Baseball Data With R/Book - First Edition/Chapter 6 - Advanced Graphics"
setwd(chapter_path)

load("balls_strikes_count.Rdata")

# The ggplot2 package
library(ggplot2)

# graphics in ggplot 2 are created by continually creating layers

# sample creates a random sample
sampleRows <- sample(1:nrow(cabrera), 20)
cabrera[sampleRows,]

# Creating a spray chart for Miguel Cabrera

# This is a ggplot object and allows for other layers to be added
p0 <- ggplot(data=cabrera, aes(x=hitx, y=hity))

# We add all of the points to the plot
p1 <- p0 + geom_point()

# Group by whether the result was a hit, error, or out. coord_equla makes an
# equal scale
p0 = ggplot(data=cabrera, aes(x=hitx, y=hity))
p1 <- p0 + geom_point(aes(color=hit_outcome))
p2 <- p1 + coord_equal()

# We can create multipanel by year through facet_wrap
p3 <- p2 + facet_wrap(~ season)

# Define location of bases
bases <- data.frame(x=c(0, 90/sqrt(2), 0, - 90/sqrt(2), 0),
                    y=c(0, 90/sqrt(2), 2*90/sqrt(2), 90/sqrt(2), 0))

# add base bath lines
p4 <- p3 + geom_path(aes(x=x, y=y), data=bases)

# Add foul lines
p4 + geom_segment(x=0, xend=300, y=0, yend=300) + 
  geom_segment(x=0, xend=-300, y=0, yend=300)


# Plot results of Cabrera's balls in play according after August accoring to
# pitch type -> color, pitch speed -> size, pitch outcome -> shape
cabreraStretch <- subset(cabrera, gamedate > "2012-08-31")
p0 <- ggplot(data=cabreraStretch, aes(hitx, hity))
p1 <- p0 + geom_point(aes(shape=hit_outcome, colour=pitch_type, size=speed))
p2 <- p1 + coord_equal()
p3 <- p2 + geom_path(aes(x=x, y=y), data=bases)
p4 <- p3 + guides(col=guide_legend(ncol=2))
p4 + geom_segment(x=0, xend=300, y=0, yend=300) + 
  geom_segment(x=0, xend=-300, y=0, yend=300)

# Create Verlander Scatterplot with Smoothing Curve

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# We will stop with this section because the code no longer works due to
# changes in the ggplot2 package

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
F4verl <- subset(verlander, pitch_type=="FF")
ggplot(F4verl, aes(pitches, speed)) + facet_wrap(~ season) +
  geom_line(stat="hline", yintercept="mean", lty=3) + 
  geom_point(aes(pitches, speed),
             data=F4verl[sample(1:nrow(F4verl), 1000),]) +
  geom_smooth(col="black") + 
  geom_vline(aes(xintercept=100), col="black", lty=2)
    

