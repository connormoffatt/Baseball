rm(list=ls())

chapter_path = "C:/Users/conno/Documents/GitHub/Baseball/Analyzing Baseball Data With R/Book - First Edition/Chapter 6 - Advanced Graphics"
setwd(chapter_path)

load("balls_strikes_count.Rdata")

# The lattice package
library(lattice)

# The Verlander dataset has 5 years of pitchfx data for Verlander

# sample creates a random sample
sampleRows <- sample(1:nrow(verlander), 20)
verlander[sampleRows,]

# display histogram and desnity plot of verlander's velocity
histogram(~ speed, data=verlander)

# plot.points = FALSE, removes points from being plotted on the x axis
densityplot(~ speed, data=verlander, plot.points=FALSE)

# Multipanel conditioning density plot based on pitchtype
densityplot(~ speed | pitch_type, data=verlander, layout=c(1,5), 
            plot.points=FALSE)

# Superimpose density plots
densityplot(~ speed, data=verlander, groups=pitch_type, plot.points=FALSE)

# Verlander four seam fastball over time for different years
F4verl <- subset(verlander, pitch_type=="FF")
F4verl$gameDay <- as.integer(format(F4verl$gamedate, format="%j"))
dailyspeed <- aggregate(speed ~ gameDay + season, data=F4verl, FUN=mean)

# scatter plot of speeds of fastball over time
xyplot(speed ~ gameDay | factor(season), data=dailyspeed, 
       xlab="Day of Year", ylab="Velocity")

# Calculate average speed of four-seam and changeup per  season. 
speedFC <- subset(verlander, pitch_type %in% c("FF", "CH"))
avgspeedFC <- aggregate(speed ~ pitch_type + season, data=speedFC, FUN=mean)
# Drop unnecessar levels
avgspeedFC <- droplevel(avgspeedFC)

# Create dotplots of changeup and four seam speed
dotplot(factor(season) ~ speed, groups=pitch_type, data=avgspeedFC, 
        pch=c("C", "F"), cex=2)

# Check Verlander's four-seam speed as the game increases
avgSpeed = aggregate(speed ~ pitches + season, data=F4verl, FUN=mean)
xyplot(speed ~ pitches | factor(season), data=avgSpeed)
avgSpeedComb <- mean(F4verl$speed)

# add a panel funciton in order to add a label and text
xyplot(speed ~ pitches | factor(season), data=avgSpeed,
       panel=function(...){
         panel.xyplot(...)
         panel.abline(v=100, lty='dotted')
         panel.abline(h=avgSpeedComb)
         panel.text(25, 100, "avg.speed")
         panel.arrows(25, 99.5, 0, avgSpeedComb, length=0.1)
       })

# Plot pitch locations for Verlander's second no hitter
NoHit <- subset(verlander, gamedate=="2011-05-07")

xyplot(pz ~ px | batter_hand, data=NoHit, groups=pitch_type, auto.key=TRUE)

# Create isometric scales because both are in feet
xyplot(pz ~ px | batter_hand, data=NoHit, groups=pitch_type, auto.key=TRUE,
       aspect="iso")

# Add labels and plot limits
xyplot(pz ~ px | batter_hand, data=NoHit, groups=pitch_type, auto.key=TRUE,
       aspect="iso",
       xlim=c(-2.2, 2.2),
       ylim=c(0, 5),
       xlab="Horizontal Location\n(ft. from middle of plate)",
       ylab="Vertical Location\n(ft. from ground)")

# Create pitch names and key for a legend
pitchnames <- c("change-up", "curveball", "4S-fastball", "2S-fastball", 
                "slider")
mykey <- list(space="right",
              border=TRUE,
              cex.title=0.8,
              title="pitch type",
              text=pitchnames,
              padding.text=4)

# Define limits of srike zone
topKzone <- 3.5
botKzone <- 1.6
inKzone <- -0.95
outKzone <- 0.95

# Plot with K zone and better legend
xyplot(pz ~ px | batter_hand, data=NoHit, groups=pitch_type, auto.key=mykey,
       aspect="iso",
       xlim=c(-2.2, 2.2),
       ylim=c(0, 5),
       xlab="Horizontal Location\n(ft. from middle of plate)",
       ylab="Vertical Location\n(ft. from ground)",
       panel=function(...){
         panel.xyplot(...)
         panel.rect(inKzone, botKzone, outKzone, topKzone, border="black", 
                    lty=3)
       })
