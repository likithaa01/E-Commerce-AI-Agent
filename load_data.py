import pandas as pd
import sqlite3

# Paths to your CSV files
ad_sales_csv = "Product-Level Ad Sales and Metrics (mapped) - Product-Level Ad Sales and Metrics (mapped).csv"
total_sales_csv = "Product-Level Total Sales and Metrics (mapped) - Product-Level Total Sales and Metrics (mapped).csv"
eligibility_csv = "Product-Level Eligibility Table (mapped) - Product-Level Eligibility Table (mapped).csv"

# Connect to SQLite database (creates it if not exists)
conn = sqlite3.connect("ecommerce.db")

# Load CSV files into Pandas DataFrames
df_ad_sales = pd.read_csv(ad_sales_csv)
df_total_sales = pd.read_csv(total_sales_csv)
df_eligibility = pd.read_csv(eligibility_csv)

# Store DataFrames as SQL tables
df_ad_sales.to_sql("ad_sales_metrics", conn, if_exists="replace", index=False)
df_total_sales.to_sql("total_sales_metrics", conn, if_exists="replace", index=False)
df_eligibility.to_sql("eligibility_table", conn, if_exists="replace", index=False)

conn.close()
print("✅ All datasets have been converted to SQL tables in ecommerce.db")
