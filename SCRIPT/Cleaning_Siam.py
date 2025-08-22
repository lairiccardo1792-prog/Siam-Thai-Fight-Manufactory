# Import libraries
import numpy as np
import pandas as pd
import requests

# Import tables
s = pd.read_csv('D:\Boolean\Progetto finale\sales_raw.csv')
p = pd.read_csv('D:\Boolean\Progetto finale\products_raw.csv')

########## Sales Data Cleaning ##########

# Drop rows with null values in 'country' and 'continent'
s = s.dropna(subset=['country', 'continent'])

# Drop duplicate rows
s = s.drop_duplicates(subset=['sale_id'], keep='first').reset_index(drop=True)

# Remove currency symbol 'THB'
s['revenue'] = (s['revenue'].astype(str).str.replace(' THB', '').astype(float))
s['loss_due_to_discount'] = (s['loss_due_to_discount'].astype(str).str.replace(' THB', '').astype(float))
s['margin'] = (s['margin'].astype(str).str.replace(' THB', '').astype(float))

# Convert currency to USD
url = 'https://api.exchangerate.host/historical?access_key=f3076df602e0496fd5e7fde27487de00&date=2024-01-01&source=THB'
r = requests.get(url)
USD = r.json()['quotes']['THBUSD']
s['revenue'] = (s['revenue'] * USD).round(2)
s['loss_due_to_discount'] = (s['loss_due_to_discount'] * USD).round(2)
s['margin'] = (s['margin'] * USD).round(2)
s = s.rename(columns={'revenue': 'revenue_usd'})
s = s.rename(columns={'margin': 'margin_usd'})

# Group some channels under 'channel'
idx = s[s['channel'] == 'App'].index 
s.loc[idx, 'channel'] = 'Online'
idx2 = s[s['channel'] == 'Shop'].index
s.loc[idx2, 'channel'] = 'Distributor'
idx3 = s[s['channel'] == 'Supplier'].index
s.loc[idx3, 'channel'] = 'Distributor'
idx4 = s[s['channel'] == 'Retail '].index
s.loc[idx4, 'channel'] = 'Retail'

# Change datatype of 'sale_date' column
s["sale_date"] = pd.to_datetime(s["sale_date"], format="%d/%m/%Y")

# Save cleaned sales data to CSV
s.to_csv('sales_modified.csv', index=False)


########## Products Data Cleaning ##########

# Drop duplicate rows
p = p.drop_duplicates(subset=['product_id'], keep='first').reset_index(drop=True)

# Remove currency symbol 'THB'
p['price'] = (p['price'].astype(str).str.replace(' THB', '').astype(float))
p['cost'] = (p['cost'].astype(str).str.replace(' THB', '').astype(float))

# Convert currency to USD
p['price'] = (p['price'] * USD).round(2)
p['cost'] = (p['cost'] * USD).round(2)
p = p.rename(columns={'price': 'price_usd'})
p = p.rename(columns={'cost': 'cost_usd'})

# Change datatype of 'release_date' column
p["release_date"] = pd.to_datetime(p["release_date"], format="%d/%m/%Y")

# Save cleaned products data to CSV
p.to_csv('products_modified.csv', index=False)
