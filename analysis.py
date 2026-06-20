"""
analysis.py
Retail Sales Analysis — Data Cleaning, EDA & Visualization

Project for: Mohd Zunaid (Aspiring Data Analyst)
Objective: Clean a raw retail sales export, explore it, and uncover
actionable insights for regional and category-level sales performance.

Run with: python3 analysis.py
"""

import pandas as pd
import matplotlib.pyplot as plt

pd.set_option("display.width", 120)

# ---------------------------------------------------------------
# STEP 1: LOAD DATA
# ---------------------------------------------------------------
df = pd.read_csv("data/retail_sales_raw.csv", parse_dates=["OrderDate"])
print("Raw shape:", df.shape)
print("\nMissing values per column:\n", df.isnull().sum())
raw_duplicate_count = df.duplicated().sum()
print("\nDuplicate rows:", raw_duplicate_count)

# ---------------------------------------------------------------
# STEP 2: DATA CLEANING
# ---------------------------------------------------------------

# 2a. Remove exact duplicate rows
df = df.drop_duplicates()

# 2b. Standardize text casing (raw exports often mix "north" / "North")
df["Region"] = df["Region"].str.strip().str.title()
df["Category"] = df["Category"].str.strip().str.title()
df["CustomerType"] = df["CustomerType"].str.strip().str.title()

# 2c. Handle missing Quantity / UnitPrice
#     Strategy: fill missing Quantity with the median quantity for that Category
#     (more accurate than a global median), and drop rows still missing UnitPrice
#     since price can't be reliably estimated.
df["Quantity"] = df.groupby("Category")["Quantity"].transform(
    lambda x: x.fillna(x.median())
)
df = df.dropna(subset=["UnitPrice"]).copy()

# 2d. Recalculate Sales after cleaning (don't trust the raw column)
df["Sales"] = df["Quantity"] * df["UnitPrice"]

# 2e. Add a Month column for trend analysis
df["Month"] = df["OrderDate"].dt.to_period("M").astype(str)

print("\nClean shape:", df.shape)
print("Missing values after cleaning:\n", df.isnull().sum())

df.to_csv("data/retail_sales_clean.csv", index=False)

# ---------------------------------------------------------------
# STEP 3: EXPLORATORY DATA ANALYSIS
# ---------------------------------------------------------------

total_sales = df["Sales"].sum()
total_orders = df["OrderID"].nunique()
avg_order_value = df["Sales"].mean()

print(f"\nTotal Sales: ₹{total_sales:,.0f}")
print(f"Total Orders: {total_orders}")
print(f"Average Order Value: ₹{avg_order_value:,.0f}")

sales_by_region = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
sales_by_category = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
monthly_sales = df.groupby("Month")["Sales"].sum().sort_index()
sales_by_customer_type = df.groupby("CustomerType")["Sales"].sum()

print("\nSales by Region:\n", sales_by_region)
print("\nSales by Category:\n", sales_by_category)
print("\nSales by Customer Type:\n", sales_by_customer_type)

top_region = sales_by_region.idxmax()
top_category = sales_by_category.idxmax()
best_month = monthly_sales.idxmax()

# ---------------------------------------------------------------
# STEP 4: VISUALIZATIONS
# ---------------------------------------------------------------
plt.style.use("seaborn-v0_8-whitegrid")

# Chart 1: Monthly sales trend
plt.figure(figsize=(9, 5))
plt.plot(monthly_sales.index, monthly_sales.values, marker="o", linewidth=2, color="#2563eb")
plt.title("Monthly Sales Trend (2023)", fontsize=14, fontweight="bold")
plt.xlabel("Month")
plt.ylabel("Sales (Rs.)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/monthly_sales_trend.png", dpi=150)
plt.close()

# Chart 2: Sales by region
plt.figure(figsize=(7, 5))
sales_by_region.plot(kind="bar", color="#16a34a")
plt.title("Total Sales by Region", fontsize=14, fontweight="bold")
plt.xlabel("Region")
plt.ylabel("Sales (Rs.)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("charts/sales_by_region.png", dpi=150)
plt.close()

# Chart 3: Sales by category
plt.figure(figsize=(7, 5))
sales_by_category.plot(kind="bar", color="#ea580c")
plt.title("Total Sales by Category", fontsize=14, fontweight="bold")
plt.xlabel("Category")
plt.ylabel("Sales (Rs.)")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("charts/sales_by_category.png", dpi=150)
plt.close()

# Chart 4: New vs Returning customer sales (pie)
plt.figure(figsize=(6, 6))
plt.pie(
    sales_by_customer_type.values,
    labels=sales_by_customer_type.index,
    autopct="%1.1f%%",
    colors=["#2563eb", "#94a3b8"],
    startangle=90,
)
plt.title("Sales Share: New vs Returning Customers", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig("charts/customer_type_share.png", dpi=150)
plt.close()

print("\nCharts saved to /charts folder.")

# ---------------------------------------------------------------
# STEP 5: KEY INSIGHTS (printed + saved to file)
# ---------------------------------------------------------------
insights = f"""
KEY INSIGHTS — Retail Sales Analysis (2023)
============================================
1. Total Sales: ₹{total_sales:,.0f} across {total_orders} orders (Avg Order Value: ₹{avg_order_value:,.0f}).
2. Top-performing region: {top_region} (₹{sales_by_region.max():,.0f} in sales).
3. Best-selling category: {top_category} (₹{sales_by_category.max():,.0f} in sales).
4. Peak sales month: {best_month}, suggesting a seasonal demand pattern worth
   investigating for inventory/staffing planning.
5. Returning customers contributed {sales_by_customer_type.get('Returning', 0) / total_sales * 100:.1f}% of total sales,
   showing the value of customer retention alongside new customer acquisition.
6. Data quality note: the raw export had {raw_duplicate_count} duplicate rows and missing
   Quantity/UnitPrice values, which were cleaned before analysis (see analysis.py Step 2).
"""
print(insights)

with open("charts/key_insights.txt", "w") as f:
    f.write(insights)
