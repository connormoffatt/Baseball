rm(list=ls())

chapter_path = "C:/Users/conno/Documents/GitHub/Baseball/Analyzing Baseball Data With R/Book - First Edition/Chapter 7 - Balls and Strikes Effects"
setwd(chapter_path)

# Behavior's by Count
load("balls_strikes_count.Rdata")
ls()

# Plot sample of where Cabrera swung
topKzone <-  3.5
botKzone <-  1.6
inKzone <- -.95
outKzone <- .95
library(lattice)

sampCabrera <- cabrera[sample(1:nrow(cabrera), 500),]
xyplot(pz ~ px, data=sampCabrera, groups=swung,
       aspect="iso",
       xlab="horizontal location (ft)",
       ylab="vertical location (ft)",
       auto.key=list(points=TRUE, text=c("no swing", "swing"), space="right"),
       panel=function(...){
         panel.xyplot(...)
         panel.rect(inKzone, botKzone, outKzone, topKzone, border="black")
       })

# Create contour plot. Start with a polynomial surface fit with loess
miggy.loess <- loess(swung ~ pz + px, data=cabrera, 
                     control=loess.control(surface="direct"))

# Create area grid
pred.area <- expand.grid(px=seq(-2, 2, 0.1), pz=seq(0, 6, 0.1))
pred.area$fit <- c(predict(miggy.loess, pred.area))

# Check how often we expect Cabrera to swing at pitches right down the middle
subset(pred.area, px==0 & pz==2.5)

# Check how often we expect Cabrera to swing at a ptichin the dirt
subset(pred.area, px==0 & pz==0)

# Check how often Cabrera swings at a pitch way outside
subset(pred.area, px==2 & pz==2.5)

# Create Contour Plots with Likelihood Cabrera Swings
contourplot(fit ~ px * pz, data=pred.area, 
             at=c(.2, .4, .6, .8),
             aspect="iso",
             xlim=c(-2, 2),
             ylim=c(0, 5),
             xlab="horizontal location (ft)",
             ylab="vertical location (ft)",
             panel=function(...){
               panel.contourplot(...)
               panel.rect(inKzone, botKzone, outKzone, topKzone, border="black",
                          lty="dotted")
             })

# Create contour plots dependent on 0-0, 2-0, and 0-2 counts
cabrera$bscount <- paste(cabrera$balls, cabrera$strikes, sep="-")

miggy00 <- subset(cabrera, bscount=="0-0")
miggy00loess <- loess(swung ~ px + pz, data=miggy00,
                     control=loess.control(surface="direct"))
pred.area$fit00 <- c(predict(miggy00loess, pred.area))

miggy02 <- subset(cabrera, bscount=="0-2")
miggy02loess <- loess(swung ~ px + pz, data=miggy02,
                      control=loess.control(surface="direct"))
pred.area$fit02 <- c(predict(miggy02loess, pred.area))

miggy20 <- subset(cabrera, bscount=="2-0")
miggy20loess <- loess(swung ~ px + pz, data=miggy20,
                      control=loess.control(surface="direct"))
pred.area$fit20 <- c(predict(miggy20loess, pred.area))

contourplot(fit00 + fit02 + fit20 ~ px * pz, data=pred.area, 
            at=c(.2, .4, .6),
            aspect="iso",
            xlim=c(-2, 2),
            ylim=c(0, 5),
            xlab="horizontal location (ft)",
            ylab="vertical location (ft)",
            panel=function(...){
              panel.contourplot(...)
              panel.rect(inKzone, botKzone, outKzone, topKzone, border="black",
                         lty="dotted")
            })

# Analyze Verlander's Pitch Selection By Count

# Get pitch frequency
table(verlander$pitch_type)

# Get pitch percentage
round(100 * prop.table(table(verlander$pitch_type)))

# Get
type_verlander_hand <- with(verlander, table(pitch_type, batter_hand))

# Margin=1 is by row and margin=2 is proportions by column
round(100 * prop.table(type_verlander_hand, margin=2))

# Get Verlander Pitch hSelection By counts
verlander$bscounts <- paste(verlander$balls, verlander$strikes, sep="-")
verl_RHB <- subset(verlander, batter_hand=="R")
verl_type_cnt_R <- table(verl_RHB$bscount, verl_RHB$pitch_type)
round(100 * prop.table(verl_type_cnt_R, margin=1))

# Check Umpires Behavior According to the Count
umpiresRHB <- subset(umpires, batter_hand=="R")
ump00 <- subset(umpiresRHB, balls==0 & strikes==0)
ump00smp <- ump00[sample(1:nrow(ump00), 3000),]
ump00.loess <- loess(called_strike ~ px + pz, data=ump00smp,
                     control=loess.control(surface="direct"))
ump00contour <- contourLines(x=seq(-2, 2, 0.1), y=seq(0, 6, 0.1),
                             z=predict(ump00.loess, pred.area), levels=c(0.5))
ump00df <- as.data.frame(ump00contour)
ump00df$bscount <- "0-0"

# 3-0
ump30 <- subset(umpiresRHB, balls==3 & strikes==0)
ump30smp <- ump00[sample(1:nrow(ump30), 3000),]
ump30.loess <- loess(called_strike ~ px + pz, data=ump30smp,
                     control=loess.control(surface="direct"))
ump30contour <- contourLines(x=seq(-2, 2, 0.1), y=seq(0, 6, 0.1),
                             z=predict(ump30.loess, pred.area), levels=c(0.5))
ump30df <- as.data.frame(ump30contour)
ump30df$bscount <- "3-0"

# 0-2
ump02 <- subset(umpiresRHB, balls==0 & strikes==0)
ump02smp <- ump00[sample(1:nrow(ump02), 3000),]
ump02.loess <- loess(called_strike ~ px + pz, data=ump00smp,
                     control=loess.control(surface="direct"))
ump02contour <- contourLines(x=seq(-2, 2, 0.1), y=seq(0, 6, 0.1),
                             z=predict(ump02.loess, pred.area), levels=c(0.5))
ump02df <- as.data.frame(ump02contour)
ump02df$bscount <- "0-2"

# Find 50% strike-calling lines
umpireContours <- rbind(ump00df, ump30df, ump02df)
trellis.par.set(theme=canonical.theme(color=FALSE))

# Create contour plot
myKey <- list(lines=TRUE,
              points=FALSE,
              space="right",
              title="Balls and Strikes Count",
              cex.title=1,
              padding=4)

xyplot(x ~ y, data=umpireContours,
       groups=bscount,
       types="l",
       aspect="iso",
       col="black",
       xlim=c(-2, 2), ylim=c(0,5),
       xlab="horizontal location (ft)",
       ylab="vertical location (ft)",
       auto.key = myKey,
       panel=function(...){
         panel.xyplot(...)
         panel.rect(inKzone, botKzone, outKzone, outKzone, border="grey70", 
                    lwd=2)
       })














