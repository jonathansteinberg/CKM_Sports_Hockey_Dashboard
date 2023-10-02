import pandas as pd
import numpy as np
import statistics as stat

### Import Total Table sheet from Final_Data
df = pd.read_excel('Final_Data.xlsx', sheet_name='Total Table')

### Drop duplciate index column, league1, and primary key
df = df.drop(columns=['Column1','League.1','PRIMARY_KEY_TEAM','InStat Index'])

### Drop test test and other Cliff mentioned
df.drop(df[df['Full Name'] == 'test test'].index, inplace = True)
df.drop(df[df['Full Name'] == 'Jake Brown'].index, inplace = True)
df.drop(df[df['Full Name'] == 'Jack Smith'].index, inplace = True)
df.drop(df[df['Full Name'] == 'Carter Davidson'].index, inplace = True)
df.drop(df[df['Full Name'] == 'Andrew Kennedy'].index, inplace = True)

### Change team fields to comparable ones
league_value_counts = df['League'].value_counts().sort_index()
print(str(len(league_value_counts))+" Leagues")

team_value_counts = df['Team'].value_counts().sort_index()
print(str(len(team_value_counts))+" Teams")

df['Team'] = df['Team'].replace('RHAW', 'RHA Winnipeg')
df['Team'] = df['Team'].replace('RHAK', 'RHA Kelowna')
df['Team'] = df['Team'].replace('SAF', 'SAR')
df['Team'] = df['Team'].replace('RDNC', 'RDC')
df['Team'] = df['Team'].replace('ACA', 'ACFRB')
df['Team'] = df['Team'].replace('Mississauga Reps', 'Mississauga Rebels')
df['Team'] = df['Team'].replace('SPS', 'SPK')

### Add secondary Number column
df['Alt Number'] = [np.nan]*len(df)

### Make seperate dataframe for Forwards and Defenseman
df_forward = df[df['Position'] == 'F']
df_defense = df[df['Position'] == 'D']

print(str(len(df['Full Name'].unique()))+" Players")

#################### FORWARDS ####################
df = df_forward

### New order of columns
columns_sum = ['Games played', 'All shifts', 
       'Time on ice in Seconds', 'Time on Ice in Minutes (INT)', 'Points',
       'Goals', 'Assists', 'First assist', 'Second assist',
       'Passes to the slot', 'Plus/Minus', 'Shots', 'Shots on goal',
       'Inner slot shots - total', 'Power play shots', 'Short-handed shots',
       'Penalties drawn', 'Penalty time in Seconds', 'Hits',
       'Blocked shots', 'Faceoffs', 'Faceoffs won', 'Faceoffs won, %',
       'Faceoffs in DZ', 'Faceoffs won in DZ', 'Faceoffs won in DZ, %',
       'Faceoffs in NZ', 'Faceoffs won in NZ', 'Faceoffs won in NZ, %',
       'Faceoffs in OZ', 'Faceoffs won in OZ', 'Faceoffs won in OZ, %']
columns_same = ['Number', 'Alt Number', 'Full Name', 'Team','Position', 'League','Age']
columns_edit = ['Time on ice','Penalty time']
df = df[columns_same+columns_sum+columns_edit]

### Dataframe of Duplicate Names
dup_name = df[df.duplicated(subset=['Full Name'], keep=False)].sort_values(by="Full Name")

### Merge Players that have Same Team Same League (57 unique names)
for name in dup_name['Full Name'].unique():
   
    dup_temp = df[df['Full Name'] == name]
    
    if dup_temp['Team'].nunique() == 1 and dup_temp['League'].nunique() == 1 and dup_temp['Number'].nunique() == 1:
        
        if len(dup_temp)>2:
            print('More than two rows')
            break
        
        columns_same_temp = dup_temp[columns_same].iloc[0,].to_list()
        columns_sum_temp = dup_temp[columns_sum].sum().to_list()
        columns_edit_temp = ['removed','removed']
        columns_all_temp = columns_same_temp+columns_sum_temp+columns_edit_temp
        
        df.drop(dup_temp.index.to_list(), inplace = True)
        new_row_df = pd.DataFrame([columns_all_temp], columns=df.columns)
        df = df.append(new_row_df, ignore_index=True)
        
    elif dup_temp['Team'].nunique() == 1 and dup_temp['League'].nunique() == 1 and dup_temp['Number'].nunique() != 1:
        
        if len(dup_temp)>2:
            print('More than two rows')
            break
    
        columns_same_temp = dup_temp[columns_same].iloc[0,].to_list()
        columns_sum_temp = dup_temp[columns_sum].sum().to_list()
        columns_edit_temp = ['removed','removed']
        columns_all_temp = columns_same_temp+columns_sum_temp+columns_edit_temp
        
        df.drop(dup_temp.index.to_list(), inplace = True)
        new_row_df = pd.DataFrame([columns_all_temp], columns=df.columns)
        new_row_df['Alt Number'] = dup_temp[columns_same].iloc[1,]['Number']
        df = df.append(new_row_df, ignore_index=True)
        
### Check Names that appear more than twice
names_more_than_twice = []
for name in dup_name['Full Name'].unique():
    dup_temp = df[df['Full Name'] == name]
    if len(dup_temp)>2:
        names_more_than_twice.append(name)
        print(dup_temp[columns_same])
        
dup_temp = df[df['Full Name'] == names_more_than_twice[0]]
dup_temp = df[df['Full Name'] == names_more_than_twice[1]]
dup_temp = df[df['Full Name'] == names_more_than_twice[2]]
dup_temp = df[df['Full Name'] == names_more_than_twice[3]]
dup_temp = df[df['Full Name'] == names_more_than_twice[4]] #remove
dup_temp = df[df['Full Name'] == names_more_than_twice[5]] #remove

names_more_than_twice =  ['Alec Nasreddine','Finn Kallay','Luke Christian',
                          'Ryder Mead']

### Names to skip over (deal with them later)
names_seperate_palyers = ['Brady Burke',
'Finn Kallay',
'Gareth Ovans',
'Harrison Owens',
'Jack Forrester',
'Kayne Huang',
'Keanan Pearman',
'Keets Fawcett',
'Matthew Sholdice',
'Mavrik Chan-Miguel',
'Oscar Lovsin',
'Sanjay Chalupiak',
'Trae Lees']

### Create special cases of names to skip over in loop
names_special_cases = []
for name in names_seperate_palyers:
    if name not in names_more_than_twice:
        names_special_cases.append(name)
names_special_cases = names_special_cases + names_more_than_twice
        

######################################################################

### Dataframe of Duplicate Names: Refresh
dup_name = df[df.duplicated(subset=['Full Name'], keep=False)].sort_values(by="Full Name")

### Pick row with most games played(62 and 75 unique names)
max_games = []
min_games = []

for name in dup_name['Full Name'].unique():
    
    dup_temp = df[df['Full Name'] == name]
    
    if dup_temp['Team'].nunique() != 1 and name not in names_special_cases: 
        
        max_games.append(dup_temp['Games played'].max())
        min_games.append(dup_temp['Games played'].min()) 
        
        if dup_temp['Games played'].max() == dup_temp['Games played'].min() and dup_temp['All shifts'].max() == dup_temp['All shifts'].min():
            df.drop(df[(df['Full Name'] == name)&(df['Time on ice in Seconds'] == dup_temp['Time on ice in Seconds'].min())].index, inplace = True)
        
        elif dup_temp['Games played'].max() == dup_temp['Games played'].min():
            df.drop(df[(df['Full Name'] == name)&(df['All shifts'] == dup_temp['All shifts'].min())].index, inplace = True)
       
        else:
            df.drop(df[(df['Full Name'] == name)&(df['Games played'] == dup_temp['Games played'].min())].index, inplace = True)
            
print("Average of most games played:",str(np.round(stat.mean(max_games),2)))
print("Average of least games played:",str(np.round(stat.mean(min_games),2)))

######################################################################

### Dataframe of Duplicate Names: Refresh
dup_name = df[df.duplicated(subset=['Full Name'], keep=False)].sort_values(by="Full Name")

### Check for remaining cases of duplciates  
for name in dup_name['Full Name'].unique():
    dup_temp = df[df['Full Name'] == name]
    if dup_temp['Team'].nunique() != 1 and dup_temp['League'].nunique() != 1 and name not in names_special_cases: 
        print(name)
        
for name in dup_name['Full Name'].unique():
    dup_temp = df[df['Full Name'] == name]
    if dup_temp['Team'].nunique() != 1 and dup_temp['League'].nunique() == 1 and name not in names_special_cases: 
        print(name)

for name in dup_name['Full Name'].unique():
    dup_temp = df[df['Full Name'] == name]
    if dup_temp['Team'].nunique() == 1 and dup_temp['League'].nunique() == 1 and name not in names_special_cases: 
        print(name)
        
######################################################################

df.replace(0,np.nan) 

df['Primary Points'] = df['Goals']+df['First assist']
df['Outter slot shots'] = df['Shots']-df['Inner slot shots - total']

df.to_excel('Player Data Forwards.xlsx')

#################### DEFENSEMEN ####################
df = df_defense

### New order of columns
columns_sum = ['Games played', 'All shifts', 
       'Time on ice in Seconds', 'Time on Ice in Minutes (INT)', 'Points',
       'Goals', 'Assists', 'First assist', 'Second assist',
       'Passes to the slot', 'Plus/Minus', 'Shots', 'Shots on goal',
       'Inner slot shots - total', 'Power play shots', 'Short-handed shots',
       'Penalties drawn', 'Penalty time in Seconds', 'Hits',
       'Blocked shots', 'Faceoffs', 'Faceoffs won', 'Faceoffs won, %',
       'Faceoffs in DZ', 'Faceoffs won in DZ', 'Faceoffs won in DZ, %',
       'Faceoffs in NZ', 'Faceoffs won in NZ', 'Faceoffs won in NZ, %',
       'Faceoffs in OZ', 'Faceoffs won in OZ', 'Faceoffs won in OZ, %']
columns_same = ['Number', 'Alt Number', 'Full Name', 'Team','Position', 'League','Age']
columns_edit = ['Time on ice','Penalty time']
df = df[columns_same+columns_sum+columns_edit]

### Dataframe of Duplicate Names
dup_name = df[df.duplicated(subset=['Full Name'], keep=False)].sort_values(by="Full Name")

### Merge Players that have Same Team Same League (57 unique names)
for name in dup_name['Full Name'].unique():
   
    dup_temp = df[df['Full Name'] == name]
    
    if dup_temp['Team'].nunique() == 1 and dup_temp['League'].nunique() == 1 and dup_temp['Number'].nunique() == 1:
        
        if len(dup_temp)>2:
            print('More than two rows')
            break
        
        columns_same_temp = dup_temp[columns_same].iloc[0,].to_list()
        columns_sum_temp = dup_temp[columns_sum].sum().to_list()
        columns_edit_temp = ['removed','removed']
        columns_all_temp = columns_same_temp+columns_sum_temp+columns_edit_temp
        
        df.drop(dup_temp.index.to_list(), inplace = True)
        new_row_df = pd.DataFrame([columns_all_temp], columns=df.columns)
        df = df.append(new_row_df, ignore_index=True)
        
    elif dup_temp['Team'].nunique() == 1 and dup_temp['League'].nunique() == 1 and dup_temp['Number'].nunique() != 1:
        
        if len(dup_temp)>2:
            print('More than two rows')
            break
    
        columns_same_temp = dup_temp[columns_same].iloc[0,].to_list()
        columns_sum_temp = dup_temp[columns_sum].sum().to_list()
        columns_edit_temp = ['removed','removed']
        columns_all_temp = columns_same_temp+columns_sum_temp+columns_edit_temp
        
        df.drop(dup_temp.index.to_list(), inplace = True)
        new_row_df = pd.DataFrame([columns_all_temp], columns=df.columns)
        new_row_df['Alt Number'] = dup_temp[columns_same].iloc[1,]['Number']
        df = df.append(new_row_df, ignore_index=True)
        
### Check Names that appear more than twice
names_more_than_twice = []
for name in dup_name['Full Name'].unique():
    dup_temp = df[df['Full Name'] == name]
    if len(dup_temp)>2:
        names_more_than_twice.append(name)
        print(dup_temp[columns_same])
        
dup_temp = df[df['Full Name'] == names_more_than_twice[0]] #merge u16
dup_temp = df[df['Full Name'] == names_more_than_twice[1]]
dup_temp = df[df['Full Name'] == names_more_than_twice[2]]
dup_temp = df[df['Full Name'] == names_more_than_twice[3]] #remove

dup_temp = df[df['Full Name'] == names_more_than_twice[0]] #merge u16
columns_same_temp = df.iloc[dup_temp.index.to_list()[1],][columns_same].to_list()
columns_sum_temp = df.iloc[dup_temp.index.to_list()[1],][columns_sum] + df.iloc[dup_temp.index.to_list()[2],][columns_sum]
columns_sum_temp = columns_sum_temp.to_list()
columns_edit_temp = ['removed','removed']
columns_all_temp = columns_same_temp+columns_sum_temp+columns_edit_temp

df.drop(dup_temp.index.to_list()[1:], inplace = True)
new_row_df = pd.DataFrame([columns_all_temp], columns=df.columns)
df = df.append(new_row_df, ignore_index=True)

names_more_than_twice =  ['Artem Frolov', 'Cooper Stockdale', 'Noah Smith']

### Names to skip over (deal with them later)
names_seperate_palyers = ['Brady Burke',
'Finn Kallay',
'Gareth Ovans',
'Harrison Owens',
'Jack Forrester',
'Kayne Huang',
'Keanan Pearman',
'Keets Fawcett',
'Matthew Sholdice',
'Mavrik Chan-Miguel',
'Oscar Lovsin',
'Sanjay Chalupiak',
'Trae Lees']

### Create special cases of names to skip over in loop
names_special_cases = []
for name in names_seperate_palyers:
    if name not in names_more_than_twice:
        names_special_cases.append(name)
names_special_cases = names_special_cases + names_more_than_twice
        

######################################################################

### Dataframe of Duplicate Names: Refresh
dup_name = df[df.duplicated(subset=['Full Name'], keep=False)].sort_values(by="Full Name")

### Pick row with most games played(62 and 75 unique names)
max_games = []
min_games = []

for name in dup_name['Full Name'].unique():
    
    dup_temp = df[df['Full Name'] == name]
    
    if dup_temp['Team'].nunique() != 1 and name not in names_special_cases: 
        
        max_games.append(dup_temp['Games played'].max())
        min_games.append(dup_temp['Games played'].min()) 
        
        if dup_temp['Games played'].max() == dup_temp['Games played'].min() and dup_temp['All shifts'].max() == dup_temp['All shifts'].min():
            df.drop(df[(df['Full Name'] == name)&(df['Time on ice in Seconds'] == dup_temp['Time on ice in Seconds'].min())].index, inplace = True)
        
        elif dup_temp['Games played'].max() == dup_temp['Games played'].min():
            df.drop(df[(df['Full Name'] == name)&(df['All shifts'] == dup_temp['All shifts'].min())].index, inplace = True)
       
        else:
            df.drop(df[(df['Full Name'] == name)&(df['Games played'] == dup_temp['Games played'].min())].index, inplace = True)
            
print("Average of most games played:",str(np.round(stat.mean(max_games),2)))
print("Average of least games played:",str(np.round(stat.mean(min_games),2)))

######################################################################

### Dataframe of Duplicate Names: Refresh
dup_name = df[df.duplicated(subset=['Full Name'], keep=False)].sort_values(by="Full Name")

### Check for remaining cases of duplciates  
for name in dup_name['Full Name'].unique():
    dup_temp = df[df['Full Name'] == name]
    if dup_temp['Team'].nunique() != 1 and dup_temp['League'].nunique() != 1 and name not in names_special_cases: 
        print(name)
        
for name in dup_name['Full Name'].unique():
    dup_temp = df[df['Full Name'] == name]
    if dup_temp['Team'].nunique() != 1 and dup_temp['League'].nunique() == 1 and name not in names_special_cases: 
        print(name)

for name in dup_name['Full Name'].unique():
    dup_temp = df[df['Full Name'] == name]
    if dup_temp['Team'].nunique() == 1 and dup_temp['League'].nunique() == 1 and name not in names_special_cases: 
        print(name)

df.drop(1541, inplace = True)

###################################################################### 

df.replace(0,np.nan)

df['Primary Points'] = df['Goals']+df['First assist']
df['Outter slot shots'] = df['Shots']-df['Inner slot shots - total']

df.to_excel('Player Data Defensemen.xlsx')
