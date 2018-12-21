import pandas as pd
import numpy as np
# Pythagorean Relationship for Other Sports

# Bill James' Pythagorean formula has been used for predicting winning 
# percentage in other sports. Since the pattern of scoring is very different
# among sports (compare for example points in basketball and goals in soccer),
# the formula needs to be adapted for the scoring environment. Find the
# necessary data for a sport of your choice and compute the optimal exponent
# to the Pythagorean formula

# https://www.basketball-reference.com/leagues/NBA_2018.html

# Data Scraping Task will be performed in python
url = 'https://www.basketball-reference.com/leagues/NBA_2018.html'
tables = pd.read_html(url)
names = ['Team', 'W', 'L', 'W/L%', 'GB', 'PS/G', 'PA/G', 'SRS']

# reset colum names and create appending dataframe between 2 conferences
tables[0].columns = names
tables[1].columns = names
standings = tables[0].append(tables[1])

# We need to calculate total points allowed and total points scored by
# multiplying by the number of games
standings['PS'] = standings['PS/G'] * 82
standings['PA'] = standings['PA/G'] * 82

# We will calculate the exponent. First we need to calculate log(W/L) and 
# the l
standings['logWratio'] = np.log(standings.W / standings.L)
standings['logPratio'] = np.log(standings.PS / standings.PA)

# Calculate linear regression through origin in order to calculate proper
# exponent. Use numpy linear algebra least squares
w = np.array(standings['logWratio'])[:, np.newaxis]
p = np.array(standings['logPratio'])
reg_coef = np.linalg.lstsq(w, p)[0]