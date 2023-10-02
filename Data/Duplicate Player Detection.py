import pandas as pd
import math
from datetime import datetime, date, timedelta

df = pd.concat(pd.read_excel('U16-U18 Canada Data (002).xlsx', sheet_name=None), ignore_index=True)

dup_name = df[df.duplicated(subset=['Full Name'], keep=False)].sort_values(by="Full Name")

dup_list = []
for name in dup_name['Full Name'].unique():
    dup_temp = df[df['Full Name'] == name]
    dup_dict = {'Name': name,
                'Duplicate Rows': len(dup_temp),
                'Same Team': dup_temp['Team'].nunique() <= 1,
                'Same League': dup_temp['League'].nunique() <= 1,
                'Same Number': dup_temp['Number'].nunique() <= 1,
                'Same Position': dup_temp['Position'].nunique() <= 1}
    dup_list.append(dup_dict)
dup_df = pd.DataFrame(dup_list)

combinations = dup_df.groupby(['Same Team', 'Same League','Same Number', 'Same Position']).size().reset_index(name='Count').sort_values(by="Count", ascending = False)
#combinations.to_excel('combinations2.xlsx')

########################################

df.columns.to_list()

df = df[['Number',
 'Full Name',
 'Team',
 'League',
 'InStat Index',
 'Position',
 'Time on ice',
 'Games played',
 'All shifts',
 'Goals',
 'First assist',
 'Second assist',
 'Assists',
 'Points',
 'Plus/Minus',
 'Inner slot shots - total',
 'Penalties drawn',
 'Penalty time',
 'Faceoffs',
 'Faceoffs won',
 'Faceoffs won, %',
 'Hits',
 'Shots',
 'Shots on goal',
 'Blocked shots',
 'Power play shots',
 'Short-handed shots',
 'Passes to the slot',
 'Faceoffs in DZ',
 'Faceoffs won in DZ',
 'Faceoffs won in DZ, %',
 'Faceoffs in NZ',
 'Faceoffs won in NZ',
 'Faceoffs won in NZ, %',
 'Faceoffs in OZ',
 'Faceoffs won in OZ',
 'Faceoffs won in OZ, %']]

xlist_dup = []
for name in dup_name['Full Name'].unique():
    dup_temp = df[df['Full Name'] == name]
    if dup_temp['Team'].nunique() != 1 and dup_temp['League'].nunique() != 1:
        xlist_dup.append(name)
print(len(xlist_dup))      
xdf_dup1 = df[df['Full Name'].isin(xlist_dup)]
xdf_dup1 = xdf_dup1.sort_values(by="Full Name")
xdf_dup1.to_excel('Different Team Different League (75 Unique Names).xlsx')
# its actually 75. Im realizing mnay of them have comparable league and team names, while ither dont 


xlist_dup = []
for name in dup_name['Full Name'].unique():
    dup_temp = df[df['Full Name'] == name]
    if dup_temp['Team'].nunique() != 1 and dup_temp['League'].nunique() == 1:
        xlist_dup.append(name)
print(len(xlist_dup))      
xdf_dup2 = df[df['Full Name'].isin(xlist_dup)]
xdf_dup2 = xdf_dup2.sort_values(by="Full Name")
xdf_dup2.to_excel('Different Team Same League (62 Unique Names).xlsx')

xlist_dup = []
for name in dup_name['Full Name'].unique():
    dup_temp = df[df['Full Name'] == name]
    if dup_temp['Team'].nunique() == 1 and dup_temp['League'].nunique() == 1:
        xlist_dup.append(name)
print(len(xlist_dup))      
xdf_dup3 = df[df['Full Name'].isin(xlist_dup)]
xdf_dup3 = xdf_dup3.sort_values(by="Full Name")
xdf_dup3.to_excel('Same Team Same League (57 Unique Players).xlsx')

xlist_dup = []
for name in dup_name['Full Name'].unique():
    dup_temp = df[df['Full Name'] == name]
    if dup_temp['Team'].nunique() == 1 and dup_temp['League'].nunique() != 1:
        xlist_dup.append(name)
print(len(xlist_dup))      
xdf_dup4 = df[df['Full Name'].isin(xlist_dup)]
xdf_dup4 = xdf_dup4.sort_values(by="Full Name")
xdf_dup4.to_excel('Same Team Different League (188 Unique Players).xlsx')

for i in xdf_dup1["Full Name"].unique():
    for j in xdf_dup2["Full Name"].unique():
        if i in j:
            print(i)

for i in xdf_dup2["Full Name"].unique():
    for j in xdf_dup3["Full Name"].unique():
        if i in j:
            print(i)

for i in xdf_dup3["Full Name"].unique():
    for j in xdf_dup4["Full Name"].unique():
        if i in j:
            print(i)

# No Overlap

########################################

df = df[['Number',
 'Full Name',
 'Team',
 'League',
 'Position',
 'InStat Index',
 'Time on ice',
 'Games played',
 'All shifts',
 'Goals',
 'First assist',
 'Second assist',
 'Assists',
 'Points',
 'Plus/Minus',
 'Inner slot shots - total',
 'Penalties drawn',
 'Penalty time',
 'Faceoffs',
 'Faceoffs won',
 'Faceoffs won, %',
 'Hits',
 'Shots',
 'Shots on goal',
 'Blocked shots',
 'Power play shots',
 'Short-handed shots',
 'Passes to the slot',
 'Faceoffs in DZ',
 'Faceoffs won in DZ',
 'Faceoffs won in DZ, %',
 'Faceoffs in NZ',
 'Faceoffs won in NZ',
 'Faceoffs won in NZ, %',
 'Faceoffs in OZ',
 'Faceoffs won in OZ',
 'Faceoffs won in OZ, %']]



xlist_dup = []
for name in dup_name['Full Name'].unique():
    dup_temp = df[df['Full Name'] == name]
    if dup_temp['Team'].nunique() != 1 and dup_temp['League'].nunique() != 1:
        xlist_dup.append(name)
print(len(xlist_dup))      
xdf_dup1 = df[df['Full Name'].isin(xlist_dup)]
xdf_dup1 = xdf_dup1.sort_values(by="Full Name")
xdf_dup1.to_excel('Different Team Different League (75 Unique Names OLD).xlsx')
# its actually 75. Im realizing mnay of them have comparable league and team names, while ither dont 
xlist_dup_sameNUM_samePOS = []
xlist_dup_sameNUM_diffPOS = []
xlist_dup_diffNUM_samePOS = []
xlist_dup_diffNUM_diffPOS = []
for name in xdf_dup1['Full Name'].unique():
    dup_temp = xdf_dup1[xdf_dup1['Full Name'] == name]
    if dup_temp['Number'].nunique() == 1 and dup_temp['Position'].nunique() == 1:
        xlist_dup_sameNUM_samePOS.append(name)
    elif dup_temp['Number'].nunique() == 1 and dup_temp['Position'].nunique() != 1:
        xlist_dup_sameNUM_diffPOS.append(name)
    elif dup_temp['Number'].nunique() != 1 and dup_temp['Position'].nunique() == 1:
        xlist_dup_diffNUM_samePOS.append(name)
    elif dup_temp['Number'].nunique() != 1 and dup_temp['Position'].nunique() != 1:
        xlist_dup_diffNUM_diffPOS.append(name)

xdf_dup1 = df[df['Full Name'].isin(xlist_dup_sameNUM_samePOS)].sort_values(by="Full Name").append(
    df[df['Full Name'].isin(xlist_dup_sameNUM_diffPOS)].sort_values(by="Full Name")).append(
        df[df['Full Name'].isin(xlist_dup_diffNUM_samePOS)].sort_values(by="Full Name")).append(
            df[df['Full Name'].isin(xlist_dup_diffNUM_diffPOS)].sort_values(by="Full Name"))
xdf_dup1.to_excel('Different Team Different League (75 Unique Names).xlsx')
print(len(xdf_dup1["Full Name"].unique()))


xlist_dup = []
for name in dup_name['Full Name'].unique():
    dup_temp = df[df['Full Name'] == name]
    if dup_temp['Team'].nunique() != 1 and dup_temp['League'].nunique() == 1:
        xlist_dup.append(name)
print(len(xlist_dup))      
xdf_dup1 = df[df['Full Name'].isin(xlist_dup)]
xdf_dup1 = xdf_dup1.sort_values(by="Full Name")
xdf_dup1.to_excel('Different Team Same League (62 Unique Names OLD).xlsx')
# its actually 75. Im realizing mnay of them have comparable league and team names, while ither dont 
xlist_dup_sameNUM_samePOS = []
xlist_dup_sameNUM_diffPOS = []
xlist_dup_diffNUM_samePOS = []
xlist_dup_diffNUM_diffPOS = []
for name in xdf_dup1['Full Name'].unique():
    dup_temp = xdf_dup1[xdf_dup1['Full Name'] == name]
    if dup_temp['Number'].nunique() == 1 and dup_temp['Position'].nunique() == 1:
        xlist_dup_sameNUM_samePOS.append(name)
    elif dup_temp['Number'].nunique() == 1 and dup_temp['Position'].nunique() != 1:
        xlist_dup_sameNUM_diffPOS.append(name)
    elif dup_temp['Number'].nunique() != 1 and dup_temp['Position'].nunique() == 1:
        xlist_dup_diffNUM_samePOS.append(name)
    elif dup_temp['Number'].nunique() != 1 and dup_temp['Position'].nunique() != 1:
        xlist_dup_diffNUM_diffPOS.append(name)

xdf_dup1 = df[df['Full Name'].isin(xlist_dup_sameNUM_samePOS)].sort_values(by="Full Name").append(
    df[df['Full Name'].isin(xlist_dup_sameNUM_diffPOS)].sort_values(by="Full Name")).append(
        df[df['Full Name'].isin(xlist_dup_diffNUM_samePOS)].sort_values(by="Full Name")).append(
            df[df['Full Name'].isin(xlist_dup_diffNUM_diffPOS)].sort_values(by="Full Name"))
xdf_dup1.to_excel('Different Team Same League (62 Unique Names).xlsx')
print(len(xdf_dup1["Full Name"].unique()))

xlist_dup = []
for name in dup_name['Full Name'].unique():
    dup_temp = df[df['Full Name'] == name]
    if dup_temp['Team'].nunique() == 1 and dup_temp['League'].nunique() == 1:
        xlist_dup.append(name)
print(len(xlist_dup))      
xdf_dup1 = df[df['Full Name'].isin(xlist_dup)]
xdf_dup1 = xdf_dup1.sort_values(by="Full Name")
xdf_dup1.to_excel('Same Team Same League (57 Unique Names OLD).xlsx')
# its actually 75. Im realizing mnay of them have comparable league and team names, while ither dont 
xlist_dup_sameNUM_samePOS = []
xlist_dup_sameNUM_diffPOS = []
xlist_dup_diffNUM_samePOS = []
xlist_dup_diffNUM_diffPOS = []
for name in xdf_dup1['Full Name'].unique():
    dup_temp = xdf_dup1[xdf_dup1['Full Name'] == name]
    if dup_temp['Number'].nunique() == 1 and dup_temp['Position'].nunique() == 1:
        xlist_dup_sameNUM_samePOS.append(name)
    elif dup_temp['Number'].nunique() == 1 and dup_temp['Position'].nunique() != 1:
        xlist_dup_sameNUM_diffPOS.append(name)
    elif dup_temp['Number'].nunique() != 1 and dup_temp['Position'].nunique() == 1:
        xlist_dup_diffNUM_samePOS.append(name)
    elif dup_temp['Number'].nunique() != 1 and dup_temp['Position'].nunique() != 1:
        xlist_dup_diffNUM_diffPOS.append(name)

xdf_dup1 = df[df['Full Name'].isin(xlist_dup_sameNUM_samePOS)].sort_values(by="Full Name").append(
    df[df['Full Name'].isin(xlist_dup_sameNUM_diffPOS)].sort_values(by="Full Name")).append(
        df[df['Full Name'].isin(xlist_dup_diffNUM_samePOS)].sort_values(by="Full Name")).append(
            df[df['Full Name'].isin(xlist_dup_diffNUM_diffPOS)].sort_values(by="Full Name"))
xdf_dup1.to_excel('Same Team Same League (57 Unique Names).xlsx')
print(len(xdf_dup1["Full Name"].unique()))

xlist_dup = []
for name in dup_name['Full Name'].unique():
    dup_temp = df[df['Full Name'] == name]
    if dup_temp['Team'].nunique() == 1 and dup_temp['League'].nunique() != 1:
        xlist_dup.append(name)
print(len(xlist_dup))      
xdf_dup1 = df[df['Full Name'].isin(xlist_dup)]
xdf_dup1 = xdf_dup1.sort_values(by="Full Name")
xdf_dup1.to_excel('Same Team Different League (188 Unique Names OLD).xlsx')
# its actually 75. Im realizing mnay of them have comparable league and team names, while ither dont 
xlist_dup_sameNUM_samePOS = []
xlist_dup_sameNUM_diffPOS = []
xlist_dup_diffNUM_samePOS = []
xlist_dup_diffNUM_diffPOS = []
for name in xdf_dup1['Full Name'].unique():
    dup_temp = xdf_dup1[xdf_dup1['Full Name'] == name]
    if dup_temp['Number'].nunique() == 1 and dup_temp['Position'].nunique() == 1:
        xlist_dup_sameNUM_samePOS.append(name)
    elif dup_temp['Number'].nunique() == 1 and dup_temp['Position'].nunique() != 1:
        xlist_dup_sameNUM_diffPOS.append(name)
    elif dup_temp['Number'].nunique() != 1 and dup_temp['Position'].nunique() == 1:
        xlist_dup_diffNUM_samePOS.append(name)
    elif dup_temp['Number'].nunique() != 1 and dup_temp['Position'].nunique() != 1:
        xlist_dup_diffNUM_diffPOS.append(name)

xdf_dup1 = df[df['Full Name'].isin(xlist_dup_sameNUM_samePOS)].sort_values(by="Full Name").append(
    df[df['Full Name'].isin(xlist_dup_sameNUM_diffPOS)].sort_values(by="Full Name")).append(
        df[df['Full Name'].isin(xlist_dup_diffNUM_samePOS)].sort_values(by="Full Name")).append(
            df[df['Full Name'].isin(xlist_dup_diffNUM_diffPOS)].sort_values(by="Full Name"))
xdf_dup1.to_excel('Same Team Different League (188 Unique Names).xlsx')
print(len(xdf_dup1["Full Name"].unique()))









































