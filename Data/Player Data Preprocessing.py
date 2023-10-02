import pandas as pd
import math
from datetime import datetime, date, timedelta

df = pd.concat(pd.read_excel('U16-U18 Canada Data (002).xlsx', sheet_name=None), ignore_index=True)

df.columns.to_list()

# Averages
averages = ['All shifts',
'Goals',
'First assist',
'Second assist',
'Assists',
'Points',
'Plus/Minus',
'Inner slot shots - total',
'Penalties drawn',
'Faceoffs',
'Faceoffs won',
'Hits',
'Shots',
'Shots on goal',
'Blocked shots',
'Power play shots',
'Short-handed shots',
'Passes to the slot',
'Faceoffs in DZ',
'Faceoffs won in DZ',
'Faceoffs in NZ',
'Faceoffs won in NZ',
'Faceoffs in OZ',
'Faceoffs won in OZ']

for a in averages:
    df[a] = df[a].replace('-',0)
    df[a] = df['Games played']*df[a]
    df[a] = df[a].round(0)
    # Not exact sums: all original averages rounded to nearest two decimals places. Solution: Make int: All decimals are either .0X or 0.9X

# Times
times = ['Time on ice',
'Penalty time']

for t in times:
    combined_list = []
    for each in df[t]:
        if each == '-':
            combined_list.append(0)
        else:
            mins = each.hour
            secs = each.minute
            seconds = (mins*60)+secs
            combined_list.append(seconds)
    df[t+' in Seconds'] = combined_list
    df[t+' in Seconds'] = df[t+' in Seconds']*df['Games played']
    
#Percentages
percentages = ['Faceoffs won, %',
'Faceoffs won in OZ, %',
'Faceoffs won in NZ, %', 
'Faceoffs won in DZ, %']
 
for p in percentages:
    df[p] = df[p].replace('-',0)
        
#Position 
df['Position'] = df['Position'].replace('Fwd','F')
df['Position'] = df['Position'].replace('Def','D')

#Age
age = []
for l in df['League']:
    if '18' in l:
        age.append('U18')
    elif '17' in l:
        age.append('U17')
    elif '16' in l:
        age.append('U16')
    elif l == 'SMAAAHL': # SMAAAHL is U18
        age.append('U18')
df['Age'] = age

#Columns order
new_columns = ['Number',
 'Full Name',
 'Team',
 'InStat Index',
 'Position',
 'League',
 'Age',
 
 'Games played',
 'All shifts',
 'Time on ice',
 'Time on ice in Seconds',
 
 'Points',
 'Goals',
 'Assists',
 'First assist',
 'Second assist',
 
 'Passes to the slot',
 
 'Plus/Minus',
 
 'Shots',
 'Shots on goal',
 'Inner slot shots - total',
 'Power play shots',
 'Short-handed shots',
 
 'Penalties drawn',
 'Penalty time',
 'Penalty time in Seconds',
 
 'Hits',
 'Blocked shots',
 
 'Faceoffs',
 'Faceoffs won',
 'Faceoffs won, %',
 'Faceoffs in DZ',
 'Faceoffs won in DZ',
 'Faceoffs won in DZ, %',
 'Faceoffs in NZ',
 'Faceoffs won in NZ',
 'Faceoffs won in NZ, %',
 'Faceoffs in OZ',
 'Faceoffs won in OZ',
 'Faceoffs won in OZ, %']

df = df[new_columns] 
    
df.to_excel('Player Data.xlsx')

