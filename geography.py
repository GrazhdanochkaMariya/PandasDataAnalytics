
import pandas as pd

# Load daat
df = pd.read_excel("main_db.xlsx", usecols=["address.data.region", "address.data.city", "address.data.area_with_type", "address.data.settlement", "opf.short"])

# Make column with unique address
df["address"] = df["address.data.region"].fillna("") + ", " + df["address.data.city"].fillna("") + ", " + df["address.data.area_with_type"].fillna("") + ", " + df["address.data.settlement"].fillna("")

# Group and count users each legal_status
df_counts = df.groupby(["address", "opf.short"]).size().reset_index(name="counts")

# Rotation
df_pivot = df_counts.pivot(index="address", columns="opf.short", values="counts").fillna(0)

# Create column 'ЮЛ'
df_pivot["ЮЛ"] = df_pivot.loc[:, df_pivot.columns != "ИП"].sum(axis=1)

# Delete needless columns
df_pivot = df_pivot[["ИП", "ЮЛ"]]

# Drop address duplicates
df_unique = df.drop_duplicates(subset=["address"])

# Merge result table with users
df_final = pd.merge(df_unique, df_pivot, on="address")

# Drop column "opf.short"
df_final.drop("opf.short", axis=1, inplace=True)

# Create column "Количество субъектов"
df_final["Количество субъектов"] = df_final[["ИП", "ЮЛ"]].sum(axis=1)

# Create column "% от общего числа"
df_final["% от общего числа"] = (df_final["Количество субъектов"] / df_final["Количество субъектов"].sum()) * 100
df_final["% от общего числа"] = df_final["% от общего числа"].round(3)

# Rename columns
df_final.rename(columns={"address.data.region": "Область", "address.data.area_with_type": "Район", "address.data.city": "Город", "address.data.settlement": "Дополнительно"}, inplace=True)

# Drop "address"
df_final.drop("address", axis=1, inplace=True)

# Save to Excel
df_final.to_excel("geography_080623.xlsx", index=False)
