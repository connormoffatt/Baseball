rm(list=ls())

chapter_path = "C:/Users/conno/Documents/GitHub/Baseball/Analyzing Baseball Data With R/Book - First Edition/Chapter 7 - Balls and Strikes Effects"
setwd(chapter_path)

# Hitter's Counts and Pitcher's Counts

# Create ball/strike frequency for Mussina
mussina <- expand.grid(balls=0:3, strikes=0:2)
mussina$value <- c(100, 118, 157, 207, 72, 82, 114, 171, 30, 38, 64, 122)

# Create heatmap function
  # second line restructures data into matrix
countmap <- function(data){
  require(plotrix)
  data <- xtabs(value ~ ., data)
  color2D.matplot(data, show.values=2, axes=FALSE, xlab="", ylab="")
  axis(side=2, at=3.5:0.5, labels=rownames(data), las=1)
  axis(side=3, at=0.5:2.5, labels=colnames(data))
  mtext(text="balls", side=2, line=2, cex.lab=1)
  mtext(text="strikes", side=3, line=2, cex.lab=1)
}
countmap(mussina)

# nchar returns the number of characters in a string
nchar("BBSBFFFX")

# Create sequences
sequences <- c("BBX", "C11BBC1S", "1X")

# grep returns indices for where match is found
grep("1", sequences)

# grepl returns boolean about matches with sequences 
grepl("1", sequences)
grepl("11", sequences)

# Can substitute values
gsub("1", "", sequences)

# Load in play by play data
pbp2011 <- read.csv("all2011.csv")
headers <- read.csv("fields.csv")
names(pbp2011) <- headers$Header

# Get pitch sequences that are actual pitches
pbp2011$pseq <- gsub("[.>123N+*]", "", pbp2011$PITCH_SEQ_TX)

# Use a regular expression to identify 1-0 and 0-1 coutns
pbp2011$c10 <- grepl("^[BIPV]", pbp2011$pseq)
pbp2011$c01 <- grepl("^[CFKLMOQRST]", pbp2011$pseq)

# load in enhanced play by play data
pbp11rc <- read.csv("pbp11rc.csv")

# get at bats that start with either 1-0 or 0-1
ab10 <- subset(pbp11rc, c10 == 1)
ab01 <- subset(pbp11rc, c01 == 1)
c(mean(ab10$RUNS.VALUE), mean(ab01$RUNS.VALUE))

# Calculate Runs Value by Every Ball Strike Count
runs.by.count <- expand.grid(balls=0:3, strikes=0:2)
runs.by.count$value <- 0

bs.count.run.value <- function(b, s){
  column.name <- paste("c", b, s, sep="")
  mean(pbp11rc[pbp11rc[, column.name] == 1, "RUNS.VALUE"])
}

# Get values for every count
runs.by.count$value <- mapply(FUN=bs.count.run.value,
                              b=runs.by.count$balls,
                              s=runs.by.count$strikes)

countmap(runs.by.count)

# Check Run Expectancy of 2-2 counts dependent on the first two pitches
count22 <- subset(pbp11rc, c22==1)
mean(count22$RUNS.VALUE)

# Get variable of count after two pitches
count22$after2 <- ifelse(count22$c20==1, "2-0", 
                         ifelse(count22$c02==1, "0-2", "1-1"))
aggregate(RUNS.VALUE ~ after2, data=count22, FUN=mean)

# Compare paths leading to 1-1 counts
count11 <- subset(pbp11rc, c11==1)
count11$after1 <- ifelse(count11$c10 == 1, "1-0", "0-1")
aggregate(RUNS.VALUE)






