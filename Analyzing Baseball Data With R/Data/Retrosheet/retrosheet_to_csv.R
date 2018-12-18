# Set the working directory to the correct folder
local_path = "C:/Users/conno/Documents/GitHub/Baseball/Analyzing Baseball Data With R/Data/Retrosheet"
setwd(local_path)

# Must create directory download.folder as subdirectory of working folder
# Then create subdirectories "zipped" and "unzipped" as a subdirectory of
# download.folder. Appropriate Chadwick files must be downloaded and placed
# in the unzipped folder:
# https://sourceforge.net/projects/chadwick/files/chadwick-0.6/chadwick-0.6.5/

# Load in the updated parsing function "parse.retrosheet2.pbp.R"
library(devtools)
source_gist(8892981)

# Loop and get all data since 2000
years <- seq(2000, 2018)
for (y in years) {
  parse.retrosheet2.pbp(y)
}