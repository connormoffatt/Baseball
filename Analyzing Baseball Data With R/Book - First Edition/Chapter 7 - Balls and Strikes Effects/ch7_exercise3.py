import pandas as pd
# Length of Plate Appearances

# Identify the baserunners who, in the 2011 season, drew the highest number
# of pickoff attempts when standing at first base with second base unoccupied

pbp2011 = pd.read_csv("all2011.csv")
headers = pd.read_csv("fields.csv")
pbp2011.columns = headers.Header

# Filter out all times 

# Create variable that removes all pitches that are not pickoffs to first
pbp2011['pickoff1'] = pbp2011['PITCH_SEQ_TX'].str.replace(
        r'[+*.23>BCFHIKLMNOPQRSTUVXY]', '', regex=True)

# Filter out when runner is only on first and not second
pbp2011 = pbp2011[~pbp2011.BASE1_RUN_ID.isna() & 
                  pbp2011.BASE2_RUN_ID.isna()]

# Create frequency table of runners
counts = pbp2011.BASE1_RUN_ID.value_counts()
counts.head()

# People that draw the most pickoff attempts (top 6)
# Ichiro Suzuki
# Michael Bourne
# Juan Pierre
# Nick Markakis
# Michael Young
# Prince Fielder

