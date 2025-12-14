import pandas as pd

#data
df0 = pd.read_csv("data/daily_sales_data_0.csv")
df1 = pd.read_csv("data/daily_sales_data_1.csv")
df2 = pd.read_csv("data/daily_sales_data_2.csv")

df = pd.concat([df0, df1, df2], ignore_index=True)

# filter Pink Morsels only
df = df[df["product"] == "pink morsel"]


df["price"] = df["price"].str.replace("$", "", regex=False).astype(float)
df["quantity"] = df["quantity"].astype(int)
df["sales"] = df["quantity"] * df["price"]
df_final = df[["sales", "date", "region"]]

df_final.to_csv("data/processed_sales_data.csv", index=False)

print("Done! File saved to: data/processed_sales_data.csv")
