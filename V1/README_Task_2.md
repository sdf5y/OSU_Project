# TASK_2_Data_Collect.ipynb

## Purpose
To collect monthly county-level labor market data for Ohio from 2000 through the most recent available year (2024). FIPS codes,  and population data from Census Bureau and economic indicators were collected from the BLS. The data was cleaned, and merged into a long-format dataset for analysis.

## Author
Sean Franco

## Date Created
2025-07-21

---

## Inputs

| File Name                                   | Description                                    | 
|---------------------------------------------|------------------------------------------------|
| `st39_oh_cou2020.txt`                       | Census FIPS county codes for Ohio              |
| `co-est00int-01-39.csv`                     | Census population estimates (2000-2010)        | 
| `co-est2020int-pop-39.xlsx`                 | Census population estimates (2010-2020)        | 
| `co-est2024-pop-39.xlsx`                    | Census population estimates (2020-2024)        | 
| `SeriesReport-20250723091941_02db8a.xlsx`   | BLS economic series data (downloaded from BLS) |

---

## Outputs

| File Name             | Description                                                           | 
|-----------------------|-----------------------------------------------------------------------|
| `bls_series.txt`      | Text file containing constructed BLS series codes for Ohio counties   |
| `OH_M_BLS_series.csv` | Final merged dataset of Ohio monthly labor market and population data | 

---

## Overview

1. **Setup**  
   - Import Python libraries and define working directories for data and outputs. 

2. **FIPS Codes**  
   - Load Ohio county-level FIPS codes from Census data and format them.

3. **BLS Series Codes**  
   - Construct BLS series IDs for the Unemployment Rate, Employment, Unemployment, and Labor Force using FIPS codes.
   - Output a text file to upload to BLS data series `bls_series.txt`.

4. **BLS Data Download**  
   - User manually download these monthly county-level economic data.

5. **BLS Data**  
   - Load BLS files and clean them by mapping indicators, cleanining year and month columns and convert to long format.
   - Merge with FIPS data by county names concatinated with year.

6. **Population Data**  
   - Download and load Census population data, then clean and append the data and convert to long format.

7. **Merge Datasets**  
   - Merge BLS economic indicators with the Census population estimates on county and year, then clean and format the columns.

8. **Output**  
   - Output a csv file of the final dataset `OH_M_BLS_series.csv`.

---

## Notes

- Government-sourced files must be downloaded and placed in the specified (data) directories.
- This notebook is part of a 2/3 interview file submission.
