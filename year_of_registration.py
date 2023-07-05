import pandas as pd
import datetime

# Load table
df = pd.read_excel('your_db.xlsx')

# Convert date in unix format to pandas date and calculate age
now = datetime.datetime.now().year
df['Возраст'] = now - pd.to_datetime(df['state.registration_date'], unit='ms').dt.year
df['Год основания'] = pd.to_datetime(df['state.registration_date'], unit='ms').dt.year

# Assign a "ЮЛ" to anything that is not a "ИП"
df['opf.short'] = df['opf.short'].apply(lambda x: 'ЮЛ' if x != 'ИП' else x)

# Group and count
grouped = df.groupby(['Год основания', 'Возраст', 'opf.short']).size().reset_index(name='Количество')

# Table conversion using the pivot_table function
table = pd.pivot_table(grouped, values='Количество', index=['Год основания', 'Возраст'], columns=['opf.short'],
                       fill_value=0)

# Save to excel
table.to_excel('registration_year_080623.xlsx')
