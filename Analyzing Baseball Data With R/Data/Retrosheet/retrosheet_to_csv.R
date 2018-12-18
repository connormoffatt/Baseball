# Set the working directory to the correct folder
local_path = "C:/Users/conno/Documents/GitHub/Baseball/Analyzing Baseball Data With R/Data/Retrosheet"
setwd(local_path)

# # Read in parse function written by Authors
# source("parse.retrosheet.pbp.R")
# 
# # Load in 1950 Data
# parse.retrosheet.pbp(1950)

# Load in the updated parsing function "parse.retrosheet2.pbp.R"
library(devtools)
source_gist(8892981)


# Loop and get all data since 2000
years <- seq(2000, 2018)
for (y in years) {
  parse.retrosheet2.pbp(y)
}