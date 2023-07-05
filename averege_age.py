import pandas as pd
import datetime

# Load data
df1 = pd.read_excel('main_data.xlsx')

# Преобразование столбца "state.registration_date" column to date format
df1['state.registration_date'] = pd.to_datetime(df1['state.registration_date'] / 1000, unit='s')

# Calculation of the current date
now = datetime.datetime.now()

# Create column "Возраст"
df1['Возраст'] = (now - df1['state.registration_date']).dt.days / 365.25

# Load okved data
df2 = pd.read_excel('okved_data.xlsx')

# Combining tables by "okved" column
df = pd.merge(df1, df2, on='okved')

# Grouping the table by "Industry/Sphere" column and calculating the average age
df = df.groupby('industry')['Возраст'].apply(lambda x: x.mean().astype(int)).reset_index()

# Save to Excel
df.to_excel('name.xlsx', index=False)
