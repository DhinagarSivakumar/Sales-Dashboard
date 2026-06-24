"""
analysis.py
-----------
Handles all data loading, cleaning, validation, and statistical analysis
for the Sales Data Analysis Dashboard.
"""

import pandas as pd
import numpy as np
import os


# ─────────────────────────────────────────────
# 1. DATA LOADING
# ─────────────────────────────────────────────

def load_data(filepath: str) -> pd.DataFrame:
    """
    Load the sales CSV file into a Pandas DataFrame.

    Parameters:
        filepath (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Raw sales data.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If the CSV is empty or missing required columns.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Data file not found: '{filepath}'")

    df = pd.read_csv(filepath)

    if df.empty:
        raise ValueError("The CSV file is empty. Please provide sales data.")

    required_columns = {"Date", "Product", "Quantity", "Price"}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"CSV is missing required columns: {missing}")

    print(f"  ✔ Loaded {len(df)} records from '{filepath}'")
    return df


# ─────────────────────────────────────────────
# 2. DATA CLEANING & VALIDATION
# ─────────────────────────────────────────────

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and validate the raw sales DataFrame.

    Steps performed:
      - Parse 'Date' column as datetime
      - Remove rows with null values
      - Remove duplicate rows
      - Ensure Quantity and Price are positive numbers
      - Add helper columns: Month, Month_Name, Revenue

    Parameters:
        df (pd.DataFrame): Raw sales data.

    Returns:
        pd.DataFrame: Cleaned and enriched DataFrame.
    """
    original_count = len(df)

    # Parse dates; invalid entries become NaT
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Drop rows with any null values (including invalid dates)
    df = df.dropna()

    # Remove exact duplicate rows
    df = df.drop_duplicates()

    # Ensure Quantity and Price are numeric and positive
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    df = df[(df["Quantity"] > 0) & (df["Price"] > 0)].dropna()

    # ── Derived columns ──────────────────────
    # Revenue = how much money each row generated
    df["Revenue"] = df["Quantity"] * df["Price"]

    # Month number (1–12) for sorting
    df["Month"] = df["Date"].dt.month

    # Month name (e.g. "Jan", "Feb") for display
    df["Month_Name"] = df["Date"].dt.strftime("%b")

    # Year (useful if dataset spans multiple years)
    df["Year"] = df["Date"].dt.year

    cleaned_count = len(df)
    removed = original_count - cleaned_count
    if removed > 0:
        print(f"  ⚠  Removed {removed} invalid/duplicate row(s) during cleaning.")
    print(f"  ✔ Data cleaned. {cleaned_count} valid records ready for analysis.")

    return df.reset_index(drop=True)


# ─────────────────────────────────────────────
# 3. ANALYSIS FUNCTIONS
# ─────────────────────────────────────────────

def calculate_total_revenue(df: pd.DataFrame) -> float:
    """Return the overall total revenue across all records."""
    return round(df["Revenue"].sum(), 2)


def calculate_monthly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate revenue by calendar month.

    Returns:
        pd.DataFrame with columns [Month, Month_Name, Revenue],
        sorted by Month (January → December).
    """
    monthly = (
        df.groupby(["Month", "Month_Name"], as_index=False)["Revenue"]
        .sum()
        .sort_values("Month")
    )
    monthly["Revenue"] = monthly["Revenue"].round(2)
    return monthly


def get_top_selling_products(df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    """
    Rank products by total quantity sold.

    Parameters:
        top_n (int): Number of top products to return (default 5).

    Returns:
        pd.DataFrame with columns [Product, Quantity], sorted descending.
    """
    top = (
        df.groupby("Product", as_index=False)["Quantity"]
        .sum()
        .sort_values("Quantity", ascending=False)
        .head(top_n)
    )
    return top


def calculate_average_order_value(df: pd.DataFrame) -> float:
    """
    Calculate the average revenue per individual transaction (row).

    Returns:
        float: Mean revenue per order, rounded to 2 decimal places.
    """
    return round(df["Revenue"].mean(), 2)


def get_best_performing_month(df: pd.DataFrame) -> dict:
    """
    Find the month with the highest total revenue.

    Returns:
        dict with keys: 'month_name', 'month_number', 'revenue'
    """
    monthly = calculate_monthly_revenue(df)
    best_row = monthly.loc[monthly["Revenue"].idxmax()]
    return {
        "month_name": best_row["Month_Name"],
        "month_number": int(best_row["Month"]),
        "revenue": round(best_row["Revenue"], 2),
    }


def calculate_revenue_by_product(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate total revenue by product (for the pie chart).

    Returns:
        pd.DataFrame with columns [Product, Revenue], sorted descending.
    """
    by_product = (
        df.groupby("Product", as_index=False)["Revenue"]
        .sum()
        .sort_values("Revenue", ascending=False)
    )
    by_product["Revenue"] = by_product["Revenue"].round(2)
    return by_product


def generate_summary_report(df: pd.DataFrame) -> None:
    """
    Print a formatted summary report to the terminal.

    Displays:
      - Dataset overview
      - Total revenue
      - Average order value
      - Best-performing month
      - Top 5 products by quantity
      - Monthly revenue breakdown
    """
    total_revenue = calculate_total_revenue(df)
    avg_order = calculate_average_order_value(df)
    best_month = get_best_performing_month(df)
    top_products = get_top_selling_products(df)
    monthly = calculate_monthly_revenue(df)

    border = "=" * 55

    print(f"\n{border}")
    print("       SALES DATA ANALYSIS — SUMMARY REPORT")
    print(border)

    # Dataset overview
    print(f"\n{'DATASET OVERVIEW':}")
    print(f"  Records analysed : {len(df)}")
    print(f"  Products tracked : {df['Product'].nunique()}")
    print(f"  Date range       : {df['Date'].min().date()} → {df['Date'].max().date()}")
    print(f"  Months covered   : {df['Month'].nunique()}")

    # Key metrics
    print(f"\n{'KEY METRICS':}")
    print(f"  Total Revenue        : ${total_revenue:>12,.2f}")
    print(f"  Average Order Value  : ${avg_order:>12,.2f}")
    print(f"  Best Month           : {best_month['month_name']} (${best_month['revenue']:,.2f})")

    # Top products
    print(f"\n{'TOP PRODUCTS BY QUANTITY SOLD':}")
    for rank, row in enumerate(top_products.itertuples(), start=1):
        print(f"  {rank}. {row.Product:<12} — {int(row.Quantity):>4} units")

    # Monthly breakdown
    print(f"\n{'MONTHLY REVENUE BREAKDOWN':}")
    for row in monthly.itertuples():
        bar_len = int(row.Revenue / monthly["Revenue"].max() * 20)
        bar = "█" * bar_len
        print(f"  {row.Month_Name:<4}  {bar:<20}  ${row.Revenue:>10,.2f}")

    print(f"\n{border}\n")
