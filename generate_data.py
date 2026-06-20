"""
generate_data.py
Creates a synthetic retail sales dataset for the Retail Sales Analysis project.
The data intentionally includes some real-world messiness (missing values,
duplicate rows, inconsistent text casing) so the cleaning step in analysis.py
has something genuine to fix.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

# ---- Reference data ----
regions = ["North", "South", "East", "West"]
categories = {
    "Electronics": ["Headphones", "Smartphone", "Laptop", "Smartwatch"],
    "Clothing": ["T-Shirt", "Jeans", "Jacket", "Shoes"],
    "Grocery": ["Rice 5kg", "Cooking Oil 1L", "Snacks Pack", "Tea 250g"],
    "Furniture": ["Office Chair", "Study Table", "Bookshelf"],
    "Stationery": ["Notebook Pack", "Pen Set", "Backpack"],
}
customer_types = ["New", "Returning"]

n_rows = 1200
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)
date_range_days = (end_date - start_date).days

rows = []
for i in range(n_rows):
    order_date = start_date + timedelta(days=int(np.random.randint(0, date_range_days)))
    category = np.random.choice(list(categories.keys()), p=[0.30, 0.25, 0.20, 0.15, 0.10])
    product = np.random.choice(categories[category])
    region = np.random.choice(regions, p=[0.30, 0.25, 0.25, 0.20])
    quantity = int(np.random.randint(1, 8))

    base_price = {
        "Electronics": np.random.randint(800, 25000),
        "Clothing": np.random.randint(300, 2500),
        "Grocery": np.random.randint(40, 400),
        "Furniture": np.random.randint(1500, 12000),
        "Stationery": np.random.randint(50, 800),
    }[category]

    customer_type = np.random.choice(customer_types, p=[0.55, 0.45])

    rows.append({
        "OrderID": 1000 + i,
        "OrderDate": order_date.strftime("%Y-%m-%d"),
        "Region": region,
        "Category": category,
        "Product": product,
        "Quantity": quantity,
        "UnitPrice": base_price,
        "CustomerType": customer_type,
    })

df = pd.DataFrame(rows)
df["Sales"] = df["Quantity"] * df["UnitPrice"]

# ---- Inject realistic messiness ----
# 1. Some missing Quantity / UnitPrice values
missing_idx = np.random.choice(df.index, size=25, replace=False)
df.loc[missing_idx[:13], "Quantity"] = np.nan
df.loc[missing_idx[13:], "UnitPrice"] = np.nan

# 2. Recompute Sales as NaN where inputs are missing (simulates a broken formula in raw export)
df["Sales"] = df["Quantity"] * df["UnitPrice"]

# 3. Inconsistent casing in Region / CustomerType (common in raw exports)
case_idx = np.random.choice(df.index, size=40, replace=False)
df.loc[case_idx, "Region"] = df.loc[case_idx, "Region"].str.lower()

# 4. Duplicate a handful of rows
dup_rows = df.sample(15, random_state=1)
df = pd.concat([df, dup_rows], ignore_index=True)

# 5. Shuffle rows so duplicates aren't all at the bottom
df = df.sample(frac=1, random_state=7).reset_index(drop=True)

df.to_csv("data/retail_sales_raw.csv", index=False)
print(f"Generated data/retail_sales_raw.csv with {len(df)} rows.")
