import pandas as pd

# Load data
df = pd.read_excel('main_db.xlsx')

# Count each legal status
value_counts = df['opf.short'].value_counts()

# Count percentage
total_count = value_counts.sum()
percentages = (value_counts / total_count * 100).round(2)

# Form new dataframe
result_df = pd.DataFrame({'Организационно-правовая форма': value_counts.index,
                          'Кол-во субъектов предпринимательства (шт)': value_counts.values,
                          'Процентное соотношение': percentages})

# Save to Excel
result_df.to_excel('name.xlsx', index=False)
