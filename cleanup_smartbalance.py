import os
import pandas as pd

# Step 1. Create a `shift` table for normalizing the scores based on Scale Score Range
idx = pd.MultiIndex.from_product([[3,4,5,6,7,8],['ELA','Math']], names=['Grade', 'Subject'])
shift = pd.DataFrame([2114,2189,2131,2204,2201,2219,2210,2235,2258,2250,2288,2265], idx, ['Point'])

# Step 2. Read "Education Directory" from following CT open data portal and extract the lat and lon
ed = pd.read_csv('Education_Directory.csv')
ed['Geo'] = ed['Location'].str.split('\n',expand=True)[2] # extract the Geo info from Location
ed[['lat','lon']] = ed['Geo'].str[1:-1].str.split(',', expand=True) # extract the lat & lon from Geo

# Step 3. Extract town income data from wikipedia   
town_income=pd.read_html('https://en.wikipedia.org/wiki/List_of_Connecticut_locations_by_per_capita_income')[2]

# Step 4. Read the manually formatted smarterbalanced.csv (see README's `Manual Data Cleaning`)
# Then we replace "*" with "" to indicate NULL and save the cleaned file as smarterbalanced_cleaned.csv
fin = open("smarterbalanced.csv", "rt")
fout = open("smarterbalanced_cleaned.csv", "wt")
for line in fin:
	fout.write(line.replace('*',''))
fin.close()
fout.close()

# Step 5. Data Cleaning 
# removing mostly blank groups: Indians and multi-racial
df = pd.read_csv('smarterbalanced_cleaned.csv', index_col=[0,1,2,3],header=[0,1])
df = df.loc[(slice(None), slice(None) , ['Asian','Black or African American','Hispanic/Latino of any race','White'])]
student_no = df.loc[(),('2021','Total Number with Scored Tests')]

# only focus on average VSS, the raw score
df = df.loc[(),(slice(None),'Average VSS')]
df['StudentNo'] = student_no
df.columns = df.columns.get_level_values(0) # `flatten` the columns

# remove the rows with all NaN
df = df[~(df['2015'].isna() & df['2016'].isna() & df['2017'].isna() & df['2018'].isna() & df['2021'].isna())]

# Step 6. Normalize the scores 
# by appending the Point column from 'shift'
df.loc[:, 'Point'] = shift.Point 

# and then subtracting the Point column from the scores
df['2015'] = df['2015'] - df['Point']
df['2016'] = df['2016'] - df['Point']
df['2017'] = df['2017'] - df['Point']
df['2018'] = df['2018'] - df['Point']
df['2021'] = df['2021'] - df['Point']
df.drop('Point',axis=1, inplace=True) # Remove the shift

df.reset_index(inplace=True) # reset the index, to be able to join

# Step 7. Data Merge
# Merge with the Education Directory to get the town, zipcode, lat & lon
ed_per_district = ed.groupby(['District Name'])[['Town','Zipcode','lat','lon']].first().reset_index().rename(columns={"District Name": "District"})
df = pd.merge(df,ed_per_district[['District','Town','Zipcode','lat','lon']], how='left', left_on='District', right_on='District')
# Merges with the Education Directory & town income data
df = pd.merge(df,town_income[['Town','Per capita income','Population']], how='left', left_on='Town', right_on='Town')
# change the currency to int
df['Per capita income'] = df[~df['Per capita income'].isna()]['Per capita income'].apply(
    lambda x: x.replace('$', '').replace(',', '') if isinstance(x, str) else x).astype(int)

# Step 8. Save the final file, and remove the intermediate file
df.to_csv("sb_final.csv")
os.remove("smarterbalanced_cleaned.csv")
