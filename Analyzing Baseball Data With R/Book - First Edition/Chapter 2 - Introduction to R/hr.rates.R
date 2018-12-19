#  Create home run rates function. Returns list of age and home run rate
hr.rates <- function(age, hr, ab){
  rates <- round(100 * hr / ab, 1)
  list(x=age, y=rates)
}