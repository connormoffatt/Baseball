rm(list=ls())

# Length of Plate Appearances

chapter_path = "C:/Users/conno/Documents/GitHub/Baseball/Analyzing Baseball Data With R/Book - First Edition/Chapter 7 - Balls and Strikes Effects"
setwd(chapter_path)

# Identify the baserunners who, in the 2011 season, drew the highest number
# of pickoff attempts when standing at first base with second base unoccupied

pbp2011 <- read.csv("all2011.csv")
headers <- read.csv("fields.csv")
names(pbp2011) <- headers$Header

# Filter out all times 

# Create variable that removes all pitches that are not pickoffs to first
pbp2011$pickoff1 <- gsub("[+*.23>BCFHIKLMNOPQRSTUVXY]", "", 
                         pbp2011$PITCH_SEQ_TX)

# Filter out when runner is only on first and not second
pbp2011 <- subset(pbp2011, BASE1_RUN_ID != "" & BASE2_RUN_ID == "")

# Create frequency table of runners
sort(table(pbp2011$BASE1_RUN_ID))

# People that draw the most pickoff attempts (top 6)
# Ichiro Suzuki
# Michael Bourne
# Juan Pierre
# Nick Markakis
# Michael Young
# Prince Fielder

