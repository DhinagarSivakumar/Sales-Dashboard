"""
visualization.py
----------------
Generates and saves all charts for the Sales Data Analysis Dashboard.

Charts produced:
  1. Monthly Revenue Trend  → line chart   (charts/monthly_revenue.png)
  2. Top Selling Products   → bar chart    (charts/top_products.png)
  3. Revenue by Product     → pie chart    (charts/revenue_pie.png)
"""

import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ── Shared style settings ────────────────────────────────────────────────────
CHART_DIR = "charts"

# Colour palette (accessible, professional)
COLORS = {
    "primary": "#2563EB",      # Blue
    "accent": "#10B981",       # Green
    "highlight": "#F59E0B",    # Amber
    "danger": "#EF4444",       # Red
    "purple": "#8B5CF6",
    "pink": "#EC4899",
    "teal": "#14B8A6",
    "pie_palette": [
        "#2563EB", "#10B981", "#F59E0B",
        "#EF4444", "#8B5CF6", "#EC4899", "#14B8A6",
    ],
}

FONT_TITLE = {"fontsize": 15, "fontweight": "bold", "color": "#111827"}
FONT_LABEL = {"fontsize": 11, "color": "#374151"}
BG_COLOR = "#F9FAFB"


def _ensure_chart_dir() -> None:
    """Create the charts/ directory if it does not exist."""
    os.makedirs(CHART_DIR, exist_ok=True)


def _save_and_close(filename: str) -> None:
    """Save the current figure to charts/ and close it."""
    _ensure_chart_dir()
    path = os.path.join(CHART_DIR, filename)
    plt.savefig(path, dpi=150, bbox_inches="tight", facecolor=BG_COLOR)
    plt.close()
    print(f"  ✔ Saved → {path}")


# ─────────────────────────────────────────────
# CHART 1 — Monthly Revenue Trend (Line Chart)
# ─────────────────────────────────────────────

def plot_monthly_revenue(monthly_df) -> None:
    """
    Draw a line chart showing revenue for each calendar month.

    Parameters:
        monthly_df (pd.DataFrame): Output of analysis.calculate_monthly_revenue().
                                   Must have columns: Month_Name, Revenue.
    """
    fig, ax = plt.subplots(figsize=(10, 5), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    months = monthly_df["Month_Name"].tolist()
    revenues = monthly_df["Revenue"].tolist()

    # ── Line + shaded area ──────────────────
    ax.plot(
        months, revenues,
        color=COLORS["primary"],
        linewidth=2.5,
        marker="o",
        markersize=7,
        zorder=3,
        label="Monthly Revenue",
    )
    ax.fill_between(
        months, revenues,
        alpha=0.12,
        color=COLORS["primary"],
    )

    # ── Annotate each data point ────────────
    for i, (month, rev) in enumerate(zip(months, revenues)):
        ax.annotate(
            f"${rev:,.0f}",
            xy=(i, rev),
            xytext=(0, 10),
            textcoords="offset points",
            ha="center",
            fontsize=8,
            color="#1D4ED8",
        )

    # ── Formatting ──────────────────────────
    ax.set_title("Monthly Revenue Trend (2024)", **FONT_TITLE, pad=14)
    ax.set_xlabel("Month", **FONT_LABEL)
    ax.set_ylabel("Revenue (USD)", **FONT_LABEL)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax.grid(axis="y", linestyle="--", alpha=0.5, color="#D1D5DB")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(fontsize=10)

    plt.tight_layout()
    _save_and_close("monthly_revenue.png")


# ─────────────────────────────────────────────
# CHART 2 — Top Selling Products (Bar Chart)
# ─────────────────────────────────────────────

def plot_top_products(top_products_df) -> None:
    """
    Draw a horizontal bar chart of the top-selling products by quantity.

    Parameters:
        top_products_df (pd.DataFrame): Output of analysis.get_top_selling_products().
                                        Must have columns: Product, Quantity.
    """
    fig, ax = plt.subplots(figsize=(9, 5), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    products = top_products_df["Product"].tolist()
    quantities = top_products_df["Quantity"].tolist()

    # Use a gradient of shades of blue
    bar_colors = [COLORS["pie_palette"][i % len(COLORS["pie_palette"])]
                  for i in range(len(products))]

    bars = ax.barh(
        products, quantities,
        color=bar_colors,
        edgecolor="white",
        linewidth=0.8,
        height=0.55,
    )

    # Label each bar with its value
    for bar, qty in zip(bars, quantities):
        ax.text(
            bar.get_width() + 1,
            bar.get_y() + bar.get_height() / 2,
            str(int(qty)),
            va="center",
            ha="left",
            fontsize=10,
            color="#111827",
        )

    ax.set_title("Top Selling Products by Quantity", **FONT_TITLE, pad=14)
    ax.set_xlabel("Total Units Sold", **FONT_LABEL)
    ax.set_ylabel("Product", **FONT_LABEL)
    ax.invert_yaxis()   # Highest at the top
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="x", linestyle="--", alpha=0.4, color="#D1D5DB")
    ax.set_xlim(0, max(quantities) * 1.18)

    plt.tight_layout()
    _save_and_close("top_products.png")


# ─────────────────────────────────────────────
# CHART 3 — Revenue Contribution by Product (Pie Chart)
# ─────────────────────────────────────────────

def plot_revenue_pie(revenue_by_product_df) -> None:
    """
    Draw a donut/pie chart showing each product's share of total revenue.

    Parameters:
        revenue_by_product_df (pd.DataFrame): Output of
            analysis.calculate_revenue_by_product().
            Must have columns: Product, Revenue.
    """
    fig, ax = plt.subplots(figsize=(8, 8), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    labels = revenue_by_product_df["Product"].tolist()
    sizes = revenue_by_product_df["Revenue"].tolist()
    total = sum(sizes)

    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct=lambda pct: f"{pct:.1f}%\n(${pct / 100 * total:,.0f})",
        colors=COLORS["pie_palette"][: len(labels)],
        startangle=140,
        pctdistance=0.78,
        wedgeprops={"edgecolor": "white", "linewidth": 2},
        # Donut effect
        radius=1.0,
    )

    # Draw the donut hole
    centre_circle = plt.Circle((0, 0), 0.55, fc=BG_COLOR)
    ax.add_patch(centre_circle)

    # Style the percentage labels
    for autotext in autotexts:
        autotext.set_fontsize(8)
        autotext.set_color("#111827")

    ax.set_title(
        "Revenue Contribution by Product",
        **FONT_TITLE,
        pad=20,
    )

    # Central annotation showing total
    ax.text(
        0, 0, f"Total\n${total:,.0f}",
        ha="center", va="center",
        fontsize=12, fontweight="bold", color="#111827",
    )

    plt.tight_layout()
    _save_and_close("revenue_pie.png")


# ─────────────────────────────────────────────
# PUBLIC ENTRY POINT
# ─────────────────────────────────────────────

def generate_all_charts(monthly_df, top_products_df, revenue_by_product_df) -> None:
    """
    Convenience function that generates all three charts in sequence.

    Parameters:
        monthly_df             : from analysis.calculate_monthly_revenue()
        top_products_df        : from analysis.get_top_selling_products()
        revenue_by_product_df  : from analysis.calculate_revenue_by_product()
    """
    print("\n  Generating charts...")
    plot_monthly_revenue(monthly_df)
    plot_top_products(top_products_df)
    plot_revenue_pie(revenue_by_product_df)
    print("  All charts saved to the 'charts/' directory.\n")
