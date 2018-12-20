import pandas as pd
import matplotlib.pyplot as plt
# Comparing Ruth, Aaron, Bonds, Arod

# (a)
# Read the Lahman "Master.csv" and "batting.csv" data files into R
people = pd.read_csv("./People.csv")
batting = pd.read_csv("./Batting.csv")

# (b)
# Use the getinfo to obtain there data frames for the season batting statistics
# for the great hitters Ty Cobb, Ted Williams, and Pete Rose

def getinfo(first, last):
    ''' Get the retrosheet player code and birth year for a player
    Arguments:
        first -> first name of player
        last -> last name of player
    
    Output:
        list that contains name code and birth year for a player'''
    player = people[people['nameFirst'] == first]
    player = player[player['nameLast'] == last]
    ix = player.index[0]
    name_code = player.at[ix, 'playerID']
    
    if player.at[ix ,'birthMonth'] <= 6:
        byear = player.at[ix, 'birthYear']
    else:
        byear = player.at[ix, 'birthYear'] + 1
    
    return [name_code, byear]

# get information for the three players  
cobb_info = getinfo("Ty", "Cobb")
williams_info = getinfo("Ted", "Williams")
rose_info = getinfo("Pete", "Rose")

# Create a dataframe of batting with the three players
cobb_data = batting[batting['playerID'] == cobb_info[0]]
williams_data = batting[batting['playerID'] == williams_info[0]]
rose_data = batting[batting['playerID'] == rose_info[0]]

# (c)
# Add the variable Age to each data frame corresponding to the ages of the three
# players
cobb_data['age'] = cobb_data['yearID'] - cobb_info[1]
williams_data['age'] = williams_data['yearID'] - williams_info[1]
rose_data['age'] = rose_data['yearID'] - rose_info[1]

# (d)
# Using the plot function, construct a line graph of the cumulative hit totals
# against age for Pete Rose\

# add cumsum hit data
cobb_data['H_sum'] = cobb_data['H'].cumsum()
williams_data['H_sum'] = williams_data['H'].cumsum()
rose_data['H_sum'] = rose_data['H'].cumsum()

fig, ax = plt.subplots()
line1 = plt.plot(rose_data['age'], rose_data['H_sum'], label='Pete Rose')
ax.set(title='Career Hits', xlabel='Age', ylabel='Hits')

# (e)
# Using the lines function, overlay the cumulative hit totals for Cobb and
# Williams
line2 = ax.plot(cobb_data['age'], cobb_data['H_sum'], label='Ty Cobb')
line3 = ax.plot(williams_data['age'], williams_data['H_sum'], 
                label='Ted Williams')
ax.legend()

# (f)
# Write a short paragraph summarizing what you have learned about the hitting
# of these three players

# We see that Pete Rose is the all time hits leader, but he played for a
# much longer time than Ty Cobb

