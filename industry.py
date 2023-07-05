import pandas as pd

# Load data
df = pd.read_excel('main_db.xlsx')
# Count each industry
result_df = df['okved_industry'].value_counts().reset_index()
result_df.columns = ['Индустрия', 'Количество']
# Save to Excel
result_df.to_excel('name.xlsx', index=False)
