"""
main.py
-------
Entry point for the Sales Data Analysis Dashboard.

Run this script from the project root:
    python src/main.py

What it does:
  1. Loads sales data from data/sales.csv
  2. Cleans and validates the dataset
  3. Runs all analysis functions
  4. Generates and saves charts to charts/
  5. Prints a summary report to the terminal
"""

import sys
import os

# Allow imports from within the src/ package when running directly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import analysis
import visualization


# ── Path configuration ───────────────────────────────────────────────────────
# Build a robust path to the CSV, regardless of where the script is called from
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "sales.csv")


def main():
    """
    Orchestrates the full pipeline:
      load → clean → analyse → visualise → report
    """
    print("\n" + "=" * 55)
    print("     SALES DATA ANALYSIS DASHBOARD")
    print("=" * 55)

    # ── Step 1: Load ─────────────────────────────────────────
    print("\n[1/4] Loading data...")
    try:
        raw_df = analysis.load_data(DATA_FILE)
    except (FileNotFoundError, ValueError) as e:
        print(f"\n  ERROR: {e}")
        print("  Please check that 'data/sales.csv' exists and is correctly formatted.")
        sys.exit(1)

    # ── Step 2: Clean ─────────────────────────────────────────
    print("\n[2/4] Cleaning & validating data...")
    try:
        df = analysis.clean_data(raw_df)
    except Exception as e:
        print(f"\n  ERROR during cleaning: {e}")
        sys.exit(1)

    # ── Step 3: Analyse ───────────────────────────────────────
    print("\n[3/4] Running analysis...")
    monthly_revenue     = analysis.calculate_monthly_revenue(df)
    top_products        = analysis.get_top_selling_products(df, top_n=7)
    revenue_by_product  = analysis.calculate_revenue_by_product(df)

    total_rev   = analysis.calculate_total_revenue(df)
    avg_order   = analysis.calculate_average_order_value(df)
    best_month  = analysis.get_best_performing_month(df)

    print(f"  ✔ Total Revenue        : ${total_rev:,.2f}")
    print(f"  ✔ Average Order Value  : ${avg_order:,.2f}")
    print(f"  ✔ Best Month           : {best_month['month_name']} (${best_month['revenue']:,.2f})")

    # ── Step 4: Visualise ─────────────────────────────────────
    print("\n[4/4] Generating visualizations...")
    try:
        visualization.generate_all_charts(monthly_revenue, top_products, revenue_by_product)
    except Exception as e:
        print(f"\n  WARNING: Could not generate one or more charts: {e}")

    # ── Summary Report ────────────────────────────────────────
    analysis.generate_summary_report(df)

    print("Dashboard complete! Open the 'charts/' folder to view your visualizations.\n")


if __name__ == "__main__":
    main()
