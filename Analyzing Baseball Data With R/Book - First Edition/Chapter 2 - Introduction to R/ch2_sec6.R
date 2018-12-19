rm(list=ls())

# Set working directory to the current chapter
chapter_path = "C:/Users/conno/Documents/GitHub/Baseball/Analyzing Baseball Data With R/Book - First Edition/Chapter 2 - Introduction to R"
setwd(chapter_path)

# Reading a dataset uses the read.csv. Docs found in comment below
# https://stat.ethz.ch/R-manual/R-devel/library/utils/html/read.table.html
spahn <- read.csv("spahn.csv")

# saving data. Use mantle data from before
HR <- c(13, 23, 21, 27, 37, 52, 34, 42, 31, 40, 54)
AB <- c(341, 549, 461, 543, 517, 533, 474, 519, 541, 527, 514)
Age <- 19:29

# cbind combines vectors of equal lengths into a matrix where the vectors are
# the columns of the matrix
source("hr.rates.R")
Mantle <- cbind(Age, HR, AB, Rates=hr.rates(Age, HR, AB)$y)

# Save created dataframe
write.csv(Mantle, "mantle.csv", row.names=FALSE)