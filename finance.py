import pandas as pd

# Load data
df_clients = pd.read_excel('main_data.xlsx')
df_okveds = pd.read_excel('okved_data.xlsx')

# Merge tables
merged_df = df_clients.merge(df_okveds, on='okved', how='left')

# Calculation of the amount of revenue by industry
industry_revenue = merged_df.groupby('industry')['bfo_2022.gainSum'].sum().reset_index()

# Rename column
industry_revenue.rename(columns={'bfo_2022.gainSum': 'Выручка (тыс. руб.)'}, inplace=True)

# Save to Excel
industry_revenue.to_excel('finance_080623.xlsx', index=False)
