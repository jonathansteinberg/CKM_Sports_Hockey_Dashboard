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
    
#Percentages
percentages = ['Faceoffs won in OZ, %',
'Faceoffs won in NZ, %', 
'Faceoffs won in DZ, %']
 
for p in percentages:
    df[p] = df[p].replace('-',0)
        
#Position 
df['Position'] = df['Position'].replace('Fwd','F')
df['Position'] = df['Position'].replace('Def','D')

df.to_excel('Sum Data.xlsx')

df2 = df.drop(["InStat Index", "Time on ice", "Full Name", "Position", 'Faceoffs won, %', 'Faceoffs won in DZ, %', 
               'Faceoffs won in NZ, %', 'Faceoffs won in OZ, %',  "Penalty time", "Number"], axis = 1)

df2 = df2.iloc[:,0:28].replace({'-': 0}, regex=True)

gp = df2.groupby(['Team', 'League']).max()["Games played"]

sums = df2.groupby(['Team', 'League']).sum()

df_raw = sums.drop(["Games played"], axis = 1)

df_raw["Games Played"] = gp

df_raw.to_excel('Full_Season_summary.xlsx')



