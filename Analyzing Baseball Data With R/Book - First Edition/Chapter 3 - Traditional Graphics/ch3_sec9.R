rm(list=ls())

# 1998 Home Run Race

chapter_path = "C:/Users/conno/Documents/GitHub/Baseball/Analyzing Baseball Data With R/Book - First Edition/Chapter 3 - Traditional Graphics"
setwd(chapter_path)

# read in 1998 play by play data and headers
data.1998 <- read.csv("all1998.csv", header=FALSE)
fields <- read.csv("fields.csv")

# Change column names in R
names(data.1998) <-  fields[,"Header"]

# Find the id for Sosa and McGwire. id's for retrosheet are in retrosheetIDs
retro.ids <- read.csv("retrosheetIDs.csv")
sosa.id <- as.character(subset(retro.ids, FIRST=="Sammy" & LAST=="Sosa")$ID)
mac.id <- as.character(subset(retro.ids, FIRST=="Mark" & LAST=="McGwire")$ID)

# Create player dataframes for every event when they were the batter
sosa.data <- subset(data.1998, BAT_ID==sosa.id)
mac.data <- subset(data.1998, BAT_ID==mac.id)

# Create function to get the date and cumulative home runs of a batter
createdata <- function(d){
  # Pull in date from the Game ID
  d$Date <- as.Date(substr(d$GAME_ID, 4, 11), format="%Y%m%d")
  # Order dtaframe rows by date
  d <- d[order(d$Date),]
  # Create Home Run Boolean and cumulative sum of home runs
  d$HR <- ifelse(d$EVENT_CD==23, 1, 0)
  d$cumHR <- cumsum(d$HR)
  
  # Return dataframe with dates
  d[, c("Date", "cumHR")]
}

# Get home run data
sosa.hr <- createdata(sosa.data)
mac.hr <- createdata(mac.data)

# Create graph of home run race. cex changes size of legend
plot(mac.hr, type="l", lwd=2, ylab="Home Runs in the Season")
lines(sosa.hr, lwd=2, col="grey")
abline(h=62, lty=3)
text(10440, 65, "62")
legend(10440, 20, legend=c("McGwire (70)", "Sosa (60)"), lwd=2, 
       col=c("black", "gray"), cex=0.75)



