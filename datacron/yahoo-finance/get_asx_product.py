import requests
import math

# Specify the URL of the .xlsx file
from datetime import datetime
from dateutil.relativedelta import relativedelta

## Specify the URL of the website
#url = "https://www.asx.com.au/connectivity-and-data/information-services/vendor-and-isv-list"
#url = "https://www.asx.com.au/asx/research/ASXListedCompanies.csv"
##url = "https://www.asx.com.au/markets/trade-our-cash-market/directory" require js to load content
##url = "https://www.marketindex.com.au/asx-listed-companies" require js to load content
#
#
## Send an HTTP GET request to the URL
#response = requests.get(url)
#
## Save the content of the webpage locally
#with open("downloaded_website.html", "w", encoding="utf-8") as file:
#    file.write(response.text)
#
#print("Website downloaded successfully!")
#
#exit()


dt_now = (datetime.now() - relativedelta(months=1)).strftime("%b-%Y").lower()
filename = f"asx-investment-products-{dt_now}-abs.xlsx"
url = f"https://www.asx.com.au/content/dam/asx/issuers/asx-investment-products-reports/2025/excel/{filename}"


# Send a GET request to download the file
response = requests.get(url)

# Save the file locally
with open(filename, "wb") as file:
    file.write(response.content)

print("File downloaded successfully!")


import pandas as pd

# Load the Excel file
file_path = filename#"path_to_your_file.xlsx"

# Load the specific tab (Spotlight ETP List)
sheet_name = "Spotlight ETP List"  # Replace with the exact tab name
df = pd.read_excel(file_path, sheet_name=sheet_name, usecols = 'B')


assert 'ASX' in df.iloc[8,0]

asx_codes = df.iloc[9:,0]#.dropna().unique()


asx_code_isallcap = asx_codes.str.isupper()

asx_cat_split = [i for i in range(len(asx_codes)) if not asx_code_isallcap.iloc[i]]
asx_cat_split.append(len(asx_codes))

store = {}
for i in range(1,len(asx_cat_split)):
    a,b = asx_cat_split[i-1]+1,asx_cat_split[i]
    
    val = [ x for x in asx_codes.iloc[a:b].tolist() if str(x) != 'nan' ] 
    if len(val):
        store[asx_codes.iloc[a-1]] = val
print(store)
#for i, code in enumerate(asx_codes):
#    if not asx_code_isallcap.iloc[i]:
#        print(f'{i: <10} {len(code): <10}"{code}"')
#        asx_cat_split.append(i)
#print(asx_code_isallcap.sum())
#print(len(asx_cat_split))
#print((~asx_code_isallcap.astype('bool',errors='ignore')).sum())