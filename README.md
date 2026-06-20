# Retail Sales Analysis — Data Cleaning, EDA & Visualization

**Author:** Mohd Zunaid
**Tools used:** Python (Pandas, NumPy), Matplotlib

## Project Overview
This project analyzes a year of retail sales transactions (1,200+ orders across 4 regions and 5 product categories) to identify regional performance, top-selling categories, and seasonal demand trends. The raw dataset was intentionally messy (missing values, duplicate rows, inconsistent text formatting) to simulate a real-world data export — the project walks through cleaning that data before analysis.

## Objective
To practice and demonstrate the core Data Analyst workflow:
**Raw Data → Clean Data → Exploratory Analysis → Visualization → Business Insight**

## Dataset
A synthetic retail sales dataset (`data/retail_sales_raw.csv`) with the following columns:
`OrderID, OrderDate, Region, Category, Product, Quantity, UnitPrice, CustomerType, Sales`

## What I Did
1. **Data Cleaning** — Removed duplicate records, standardized inconsistent text casing (e.g. "north" vs "North"), and handled missing values (filled missing Quantity using category-level medians; dropped rows with missing price since it couldn't be reliably estimated).
2. **Exploratory Data Analysis (EDA)** — Calculated total sales, average order value, and broke down performance by region, category, month, and customer type using Pandas groupby operations.
3. **Visualization** — Built 4 charts with Matplotlib: monthly sales trend, sales by region, sales by category, and new-vs-returning customer sales share.
4. **Insights** — Summarized findings into clear, actionable business takeaways (see below).

## Key Insights
- Total sales of ~₹2.5 crore across 1,188 cleaned orders, with an average order value of ~₹21,000.
- **North region** was the top performer; **West region** lagged behind, indicating an opportunity for targeted marketing.
- **Electronics** drove the majority of revenue despite Clothing and Grocery having higher order counts — showing the impact of high-value items on total revenue.
- A clear **sales spike in November**, likely tied to seasonal/festive shopping, useful for inventory and staffing planning.
- **Returning customers** contributed over 40% of total sales, highlighting the value of retention alongside new customer acquisition.

## How to Run
```bash
pip install pandas numpy matplotlib
python3 generate_data.py   # generates the raw dataset
python3 analysis.py        # cleans data, runs EDA, saves charts to /charts
```

## Files
- `generate_data.py` — creates the synthetic raw dataset
- `analysis.py` — full cleaning + EDA + visualization pipeline
- `data/retail_sales_raw.csv` — raw (messy) data
- `data/retail_sales_clean.csv` — cleaned data
- `charts/` — generated PNG visualizations and a text summary of insights

## What I'd Do Next
- Build an interactive Power BI / Tableau dashboard on top of the cleaned dataset
- Add a basic forecasting model to predict next month's sales
- Segment customers using RFM (Recency, Frequency, Monetary) analysis
