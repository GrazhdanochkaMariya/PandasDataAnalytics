

import pandas as pd

# Load data from DBs
clients = pd.read_excel('db_main.xlsx')
sectors = pd.read_excel("okveds_db.xlsx")

# Combination of data by the register number of the sphere of activity from_table
merged_data = pd.merge(clients, sectors, on='okved')

# Format the "Название сферы деятельности" column with all registry numbers
merged_data['ОКВЭД'] = merged_data['okved_name'] + ' ' + merged_data['okved'].astype(str)

# Group the data by the formatted name of the business area and count the number of users in each group
grouped_data = merged_data.groupby('ОКВЭД').size().reset_index(name='Количество')

# Count percentage
total_clients = len(clients)
grouped_data['Процент'] = grouped_data['Количество'] / total_clients * 100
grouped_data['Процент'] = grouped_data['Процент'].round(2)  # Округление до 3 знаков после запятой

# Save to excel
grouped_data.to_excel('sphere_okved_090623.xlsx', index=False)



