# Section 2.3 Vectors

# vector is a sequence of values of a given type
# Warren Spahn

# Initialize wins and losses per season
W <- c(8, 21, 15, 21, 21, 22, 14)
L <- c(5, 10, 12, 14, 17, 14, 19)

# Calculate win percentage
Win.Pct <- 100 * W / (W + L)

# Create patterned data with sequence and colon for integers
Year <- seq(1946, 1952)
Year <- 1946 : 1952

# Calculate Age from year
Age <-  Year - 1921

# Scatter plot of winning percentage and age
plot(Age, Win.Pct)

# apply various vector functions

# Average winning percentage
mean(Win.Pct)

# Career winning percentage
100 * sum(W) / (sum(W) + sum(L))

# Sort win numbers
sort(W)

# Cumulative sum of wins
cumsum(W)

# Summary stats
summary(Win.Pct)

# Index and logical variables

# Extract specific indexes
W[c(1, 2, 5)]
W[1:4]
W[-c(1,6)]

# Logic
W.Pct > 60
(W > 20) & (Win.Pct > 60)
Win.Pct == max(Win.Pct)
Year[Win.Pct == max(Win.Pct)]
Year[W + L > 30]
















