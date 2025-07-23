#!/usr/bin/env python
# coding: utf-8

# **Name:**   TASK_2_Data_Collect.ipynb   
# **Purpose:**  To collect monthly county-level labor market data for Ohio from 2000 to the most recent available year (2024).          
# **Author:**   Sean Franco   
# **Date Created:**     2025_07_21           
# **Inputs:**   5 file inputs.
# 
#             1 CENSUS Fips dataset: st39_oh_cou2020.txt;
#             
#             3 CENSUS population datasets: co-est00int-01-39.csv, co-est2020int-pop-39.xlsx, co-est2024-pop-39.xlsx; 
# 
#             1 BLS economic series dataset: SeriesReport-20250723091941_02db8a.xlsx; 
# 
# **Outputs:**  2 file outputs. 
# 
#             1 BLS code file: bls_series.txt; 
# 
#             1 Ohio data file: OH_M_BLS_series.csv  
# 
# **Notes:**  2/3 Interview file submission.            

# In[ ]:


#import libraries and packages
import numpy as np
import pandas as pd
import os


# In[ ]:


#set Working Directories 

data_dir = 'C:\\Users\\18045\\Documents\\Python\\OSU_Project\\Data'
data_pop_dir = 'C:\\Users\\18045\\Documents\\Python\\OSU_Project\\Data\\population'
data_econ_dir = 'C:\\Users\\18045\\Documents\\Python\\OSU_Project\\Data\\economic_indicators'

output_dir = 'C:\\Users\\18045\\Documents\\Python\\OSU_Project\\output'


# The first step is to download government verified data for Ohio's FIPS codes. These codes will be used to call the county-level economic series at the Bureau of Labor Statistics (BLS). Make sure to use Federal Government downloads. Do not open the file or modify it. If that occurs, then redownload the file to ensure data integrity. 
# 
# The CENSUS Bureau offers downloads of state, and county FIPS codes by selecting "County and County Equivalent Entities". Select OHIO from the dropdown, and save the txt file. 
# 
# https://www.census.gov/library/reference/code-lists/ansi.html
# 
# Alternativly, the Department of Transportation offers a download (and an API) of the FIPS codes.
# 
# https://data.transportation.gov/Railroads/State-County-and-City-FIPS-Reference-Table/eek5-pv8d/about_data
# 

# In[ ]:


#Load the Census FIPS file for Ohio
os.chdir(data_dir)

fips_df = pd.read_csv('st39_oh_cou2020.txt', sep = '|')


# In[4]:


#fill in with leading Zeros on County FIPS column 

fips_df['COUNTYFP_s'] = fips_df['COUNTYFP'].astype(str).str.zfill(3)


# Now that we have STATE, and COUNTY FIPS codes we can construct the BLS economic series codes. According to the BLS website county-level unemployement series are formated as: "LAUCN390330000000003" where "LAUCN" in the local area unemployment statistics (LAUS). The "39" refers to the State FP for OHIO, and the "033" stands for Crawford County. The "0000000003" code signifies the unemployment rate series. 
# 
# https://data.bls.gov/dataQuery/find?st=0&r=20&s=popularity%3AD&q=OH+and+unemployment+rate&fq=survey:[la]&more=0

# In[ ]:


#Construct Ohio's BLS code series into a TXT file

unemployment_rate = ('LAUCN' + fips_df['STATEFP'].astype(str) + 
                             fips_df['COUNTYFP_s'].astype(str) +  '0000000003') #Unemployment Rate

employment = ('LAUCN' + fips_df['STATEFP'].astype(str) + 
                             fips_df['COUNTYFP_s'].astype(str) +  '0000000005') #Employment

unemployment = ('LAUCN' + fips_df['STATEFP'].astype(str) + 
                             fips_df['COUNTYFP_s'].astype(str) +  '0000000004') #Unemployment

labor_force = ('LAUCN' + fips_df['STATEFP'].astype(str) + 
                             fips_df['COUNTYFP_s'].astype(str) +  '0000000006') #Labor Force


# In[ ]:


#output the BLS series TXT file
os.chdir(output_dir)

BLS_codes = (unemployment_rate.tolist() + employment.tolist() + unemployment.tolist() + labor_force.tolist())

with open('bls_series.txt', 'w') as f:
    for code in BLS_codes:
        f.write(f"{code}\n")


# Now that we have a TXT file of the 4 BLS economic series codes for each of Ohio's 88 counties. We will copy and pase the contents of the text file into the BLS's website to call the series. To ensure data quality, the TXT file should have 352 lines (aka 88 counties * 4 economic BLS series). If you are unsure about data integrity of the TXT file, then regenerate it.
# 
# https://data.bls.gov/series-report
# 
# **Step 1).** Copy and paste all economic BLS series from the TXT file into BLS's series-report page
# ![image-2.png](attachment:image-2.png)
# 
# 
# **Step 2).** Select the Multiseries table, and the specify year range of 2000 to 2025. Then retrieve data. Download the xlsx file.
# ![image-3.png](attachment:image-3.png)

# In[ ]:


#Loading the downloaded BLS file.
os.chdir(data_dir)

bls_econ_df = pd.read_excel('SeriesReport-20250723091941_02db8a.xlsx', skiprows=3)


# In[77]:


#prepare to convert to long format
indicator_map = {'003': 'Unemployment Rate', '004': 'Unemployment', '005': 'Employment', '006': 'Labor Force'}

bls_econ_df['Indicator Code'] = bls_econ_df['Series ID'].str[-3:]

bls_econ_df['Indicator'] = bls_econ_df['Indicator Code'].map(indicator_map)


# In[ ]:


#Convert BLS series to Long format
OHIO_Econ_Long_df = bls_econ_df.melt(
    id_vars=['Series ID', 'Indicator'], 
    var_name='Year', 
    value_name='Value')


# In[112]:


#drop NAs which are in th Year 2025. 352 NAs for the Year field indicates that all 4 series have incomplete information for 2025 since the year is presently occurring
print(OHIO_Econ_Long_df.isna().sum())
OHIO_Econ_Long_df.dropna(inplace=True)


# In[ ]:


#split the Year column into years and months, and split Series ID to get county FIPS codes
OHIO_Econ_Long_df['Month'] = OHIO_Econ_Long_df['Year'].astype(str).str.split('\n').str[0]

OHIO_Econ_Long_df['Year'] = OHIO_Econ_Long_df['Year'].astype(str).str.split('\n').str[1]

OHIO_Econ_Long_df['COUNTYFP'] = OHIO_Econ_Long_df['Series ID'].astype(str).str.split('LAUCN39').str[1].str.slice(0, 3)


# In[114]:


#merge with FIPS data to get county information
OHIO_Econ_Long_df = pd.merge(OHIO_Econ_Long_df, fips_df, left_on= "COUNTYFP", right_on= "COUNTYFP_s", how='left')


# In[ ]:


#keep relevant columns
OHIO_Econ_Long_df = OHIO_Econ_Long_df[['Series ID', 'COUNTYFP_x', 'Month', 'Year', 'Indicator', 'Value', 'STATE', 'STATEFP','COUNTYNAME']]

#Then clean column names
OHIO_Econ_Long_df.columns = ['Series ID', 'COUNTYFP', 'Month', 'Year', 'Indicator', 'Value', 'STATE', 'STATEFP', 'COUNTYNAME']

#DONE with Ohio economic indicators dataframe


# Monthly, county-level population series seem to not exist. Yearly county-level OHIO Population series are available via CENSUS Bureau so we'll use this instead.
# 
# The years 2000 to 2010 were downloaded using the link below:
# 
# https://www2.census.gov/programs-surveys/popest/tables/2000-2010/intercensal/county/
# 
# The years 2010 to 2020 were downloaded using the link below:
# 
# https://www2.census.gov/programs-surveys/popest/tables/2010-2020/intercensal/county/
# 
# The years 2020 to 2024 were downloaded using the link below:
# 
# https://www.census.gov/data/tables/time-series/demo/popest/2020s-counties-total.html
# 

# In[6]:


os.chdir(data_pop_dir)

population_0010_df = pd.read_csv('co-est00int-01-39.csv', skiprows = 3, skipfooter=8, engine = 'python')

population_1020_df = pd.read_excel('co-est2020int-pop-39.xlsx', skiprows=3, skipfooter=6)

population_2020_df = pd.read_excel('co-est2024-pop-39.xlsx', skiprows= 3, skipfooter=6)


# In[ ]:


#setting columns and dropping first row, and extra column in 2000-2010 population data 
population_0010_df.columns = ['Geographic Area', 'Unnamed: 1', '2000', '2001', '2002', '2003', '2004',
       '2005', '2006', '2007', '2008', '2009', 'Unnamed: 12', 'Unnamed: 13']

population_0010_df.drop(['Unnamed: 1', 'Unnamed: 12', 'Unnamed: 13'], axis=1, inplace= True)

population_0010_df.drop(index=population_0010_df.index[0], axis=0, inplace=True)

population_0010_df['Geographic Area'] = population_0010_df['Geographic Area'] + str(', Ohio')

#convert values to numeric
for col in population_0010_df.columns[1:]:
    population_0010_df[col] = population_0010_df[col].astype(str).str.replace(',', '').str.strip()

    population_0010_df[col] = pd.to_numeric(population_0010_df[col], errors='coerce')


# In[ ]:


#setting columns and dropping first row, and extra column in 2010-2020 population data 
population_1020_df.columns = [ 'Geographic Area',  'Unnamed: 1', '2010', '2011', '2012', '2013', '2014', 
                              '2015', '2016', '2017','2018', '2019', 'Unnamed: 12']

population_1020_df.drop(['Unnamed: 1', 'Unnamed: 12'], axis=1, inplace= True)

population_1020_df.drop(index=population_1020_df.index[0], axis=0, inplace=True)


# In[ ]:


#setting columns and dropping first row, and extra column in 2020-2024 population data 
population_2020_df.columns = ['Geographic Area', 'Unnamed: 1', '2020', '2021', '2022', '2023', '2024']

population_2020_df.drop('Unnamed: 1', axis=1, inplace= True)

population_2020_df.drop(index=population_2020_df.index[0], axis=0, inplace=True)


# In[ ]:


#merge CENSUS populations tables together
Population_df = pd.merge(population_0010_df, population_1020_df, on= "Geographic Area")

Population_df = pd.merge(Population_df, population_2020_df, on= "Geographic Area") 


# In[118]:


#Convert Population to Long format
OHIO_Counties_Long_df = Population_df.melt(id_vars=['Geographic Area'], var_name='Year', value_name='Population')


# In[ ]:


#clean the data types and construct a primary key
OHIO_Counties_Long_df['Geographic Area'] = OHIO_Counties_Long_df['Geographic Area'].str.replace('.', '', regex=False)

OHIO_Counties_Long_df['COUNTYNAME'] = (OHIO_Counties_Long_df['Geographic Area'].str.split(',').str[0] + ', OH' + OHIO_Counties_Long_df['Year'])

OHIO_Econ_Long_df['COUNTYNAME_merge'] = (OHIO_Econ_Long_df['COUNTYNAME'] + ', OH' + OHIO_Econ_Long_df['Year'])


# Final steps below to merge the Economic indicators and Population Dataframes, to clean the data types then to save the results as a .csv file.

# In[142]:


#merge the Economic Indicators and Population dataframes
OH_Month_series = pd.merge(OHIO_Econ_Long_df, OHIO_Counties_Long_df, left_on= 'COUNTYNAME_merge', right_on= 'COUNTYNAME', how= 'left')


# In[ ]:


#Select columns, rename, and rearrange. Remove NAs for 2025, then create a Date column. 
OH_Month_series = OH_Month_series[['Series ID', 'STATE', 'STATEFP', 'COUNTYNAME_x','COUNTYFP', 'Month', 'Year_x', 'Indicator', 'Value', 'Population']]

OH_Month_series.columns = ['Series ID', 'STATE', 'STATEFP', 'COUNTYNAME','COUNTYFP', 'Month', 'Year', 'Indicator', 'Value', 'Population']

OH_Month_series = OH_Month_series.dropna() #nas in the year 2025.

OH_Month_series['Date'] = pd.to_datetime(OH_Month_series['Year'].astype(str) + '-' + OH_Month_series['Month'], format='%Y-%b')

OH_Month_series = OH_Month_series[['Series ID', 'STATE', 'STATEFP', 'COUNTYNAME', 'COUNTYFP', 'Month',
       'Year', 'Date', 'Indicator', 'Value', 'Population']]


# In[ ]:


#setting the data types
OH_Month_series['STATEFP'] = OH_Month_series['STATEFP'].astype(str).str.zfill(2)

OH_Month_series['Year'] = pd.to_numeric(OH_Month_series['Year'], errors='coerce').astype('Int64')

OH_Month_series['Value'] = pd.to_numeric(OH_Month_series['Value'], errors='coerce')

for col in ['Series ID', 'STATE', 'COUNTYNAME', 'Month', 'Indicator']:
    OH_Month_series[col] = OH_Month_series[col].astype('category')


# In[ ]:


#save the results
os.chdir(output_dir)
OH_Month_series.to_csv('OH_M_BLS_series.csv', index=False)


# END of Script.
