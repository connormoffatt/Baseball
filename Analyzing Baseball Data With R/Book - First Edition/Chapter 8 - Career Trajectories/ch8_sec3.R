  rm(list=ls())
  
  chapter_path = "C:/Users/conno/Documents/GitHub/Baseball/Analyzing Baseball Data With R/Book - First Edition/Chapter 8 - Career Trajectories"
  setwd(chapter_path)
  
  Fielding <- read.csv("Fielding.csv")
  Batting <- read.csv("Batting.csv")
  
  People <- read.csv("People.csv")
  
  mantle.info <- subset(People, nameFirst=="Mickey" & nameLast=="Mantle")
  mantle.id <- as.character(mantle.info$playerID)
  
  # Analyze trajectories by position
  
  # First only get batters with 2000 Career PA
  library(plyr)
  AB.totals <- ddply(Batting, .(playerID), summarize, 
                     Career.AB=sum(AB, na.rm=TRUE))
  Batting <- merge(Batting, AB.totals)
  Batting.2000 <- subset(Batting, Career.AB > 2000)
  
  # Create function to find a player's most common position
  find.position <- function(p){
    positions <- c("OF", "1B", "2B", "3B", "SS", "C", "P", "DH")
    d <- subset(Fielding, playerID==p)
    count.games <- function(po)
      sum(subset(d, POS==po)$G)
    FLD <- sapply(positions, count.games)
    positions[FLD == max(FLD)][1]
  }
  
  # Create dataframe with fielding positions and playerIDs for players > 2000 PA
  PLAYER <- as.character(unique(Batting.2000$playerID))
  POSITIONS <- sapply(PLAYER, find.position)
  Fielding.2000 <- data.frame(playerID=names(POSITIONS), POS=POSITIONS)
  Batting.2000 <- merge(Batting.2000, Fielding.2000)
  
  # Calculate Career Statistics
  C.totals <- ddply(Batting.2000, .(playerID), summarize,
                    C.G=sum(G, na.rm=TRUE),
                    C.AB=sum(AB, na.rm=TRUE),
                    C.R=sum(R, na.rm=TRUE),
                    C.H=sum(H, na.rm=TRUE),
                    C.2B=sum(X2B, na.rm=TRUE),
                    C.3B=sum(X3B, na.rm=TRUE),
                    C.HR=sum(HR, na.rm=TRUE),
                    C.RBI=sum(RBI, na.rm=TRUE),
                    C.BB=sum(BB, na.rm=TRUE),
                    C.SO=sum(SO, na.rm=TRUE),
                    C.SB=sum(SB, na.rm=TRUE))
  
  # Calculalte batting and slugging
  C.totals$C.AVG <- with(C.totals, C.H / C.AB)
  C.totals$C.SLG <- with(C.totals, C.H - C.2B - C.3B - C.HR + 2*C.2B + 3*C.3B 
                         + 4*C.HR)
  
  # Compute Career totals with fielding totals. Each position is given an
  # associated fielding value for similarity scores
  C.totals <- merge(C.totals, Fielding.2000)
  C.totals$VALUE.POS <- with(C.totals,
                   ifelse(POS=="C", 240,
                   ifelse(POS=="SS", 168,
                   ifelse(POS=="2B", 132,
                   ifelse(POS=="3B", 84,
                   ifelse(POS=="OF", 48,
                   ifelse(POS=="1B", 12, 0)))))))
  
  # Computing Bill James Similarity Score
  similar <- function(p, number=10){
    P <- subset(C.totals, playerID==p)
    C.totals$SS <- with(C.totals,
                       1000 -
                       floor(abs(C.G - P$C.G) / 20) -
                       floor(abs(C.AB - P$C.AB) / 75) - 
                       floor(abs(C.R - P$C.R) / 10) -  
                       floor(abs(C.H - P$C.H) / 15) - 
                       floor(abs(C.2B - P$C.2B) / 5) - 
                       floor(abs(C.3B - P$C.3B) / 4) - 
                       floor(abs(C.HR - P$C.HR) / 2) - 
                       floor(abs(C.RBI - P$C.RBI) / 10) - 
                       floor(abs(C.BB - P$C.BB) / 25) - 
                       floor(abs(C.SO - P$C.SO) / 150) - 
                       floor(abs(C.SB - P$C.SB) / 20) - 
                       floor(abs(C.AVG - P$C.AVG) / 0.001) - 
                       floor(abs(C.SLG - P$C.SLG) / 0.002) - 
                       abs(VALUE.POS - P$VALUE.POS))
    C.totals <- C.totals[order(C.totals$SS, decreasing=TRUE),]
    C.totals[1:number,]
  }
  similar(mantle.id, 6)
