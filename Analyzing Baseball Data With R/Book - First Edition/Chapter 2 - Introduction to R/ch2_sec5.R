rm(list=ls())

# Can create your own function
# Name.of.function <- function(arguments) {}
source("hr.rates.R")

# Can read this directly into the editor or we can save it in its own file
# and then call it in using scource("hr.rates.R")

# Use function on some manually entered Mickey Mantle Data
HR <- c(13, 23, 21, 27, 37, 52, 34, 42, 31, 40, 54)
AB <- c(341, 549, 461, 543, 517, 533, 474, 519, 541, 527, 514)
Age <- 19:29
hr.rates(Age, HR, AB)

# Now we create a scatterplot
plot(hr.rates(Age, HR, AB))
