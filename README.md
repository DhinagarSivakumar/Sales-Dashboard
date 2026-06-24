# 📊 Sales Data Analysis Dashboard

A beginner-to-intermediate Python project that loads, cleans, analyses, and visualises retail sales data — producing publication-ready charts and a terminal summary report.

Built as a portfolio project to demonstrate real-world data analysis skills using **Pandas**, **Matplotlib**, and Python best practices.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📥 Data Loading | Reads sales records from a CSV file with validation |
| 🧹 Data Cleaning | Handles nulls, duplicates, and invalid types automatically |
| 💰 Total Revenue | Computes overall revenue across all transactions |
| 📅 Monthly Trends | Aggregates and ranks revenue by calendar month |
| 🏆 Top Products | Ranks products by total units sold |
| 🧾 Average Order | Calculates mean revenue per transaction |
| 🌟 Best Month | Identifies the highest-revenue month |
| 📈 Line Chart | Monthly revenue trend visualisation |
| 📊 Bar Chart | Top-selling products by quantity |
| 🥧 Pie Chart | Revenue contribution (%) per product |
| 🖨️ Terminal Report | Formatted summary report with ASCII bar chart |

---

## 🗂 Project Structure

```
Sales-Dashboard/
│
├── data/
│   └── sales.csv           ← Input dataset (Date, Product, Quantity, Price)
│
├── charts/                 ← Auto-created; all PNGs saved here
│   ├── monthly_revenue.png
│   ├── top_products.png
│   └── revenue_pie.png
│
├── src/
│   ├── analysis.py         ← Data loading, cleaning & statistical functions
│   ├── visualization.py    ← All Matplotlib chart generation
│   └── main.py             ← Entry point — runs the full pipeline
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🛠 Technologies Used

- **Python 3.x** — Core language
- **Pandas** — Data manipulation and aggregation
- **Matplotlib** — Chart generation
- **NumPy** — Numerical support
- **CSV** — Lightweight data storage format

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/Sales-Dashboard.git
cd Sales-Dashboard
```

### 2. (Recommended) Create a virtual environment
```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

From the project root directory:
```bash
python src/main.py
```

The script will:
1. Load and clean `data/sales.csv`
2. Run all analysis functions
3. Save three charts to the `charts/` folder
4. Print a summary report in the terminal

---

## 📸 Example Output

### Terminal Report
```
=======================================================
       SALES DATA ANALYSIS — SUMMARY REPORT
=======================================================

DATASET OVERVIEW
  Records analysed : 128
  Products tracked : 7
  Date range       : 2024-01-03 → 2024-08-31
  Months covered   : 8

KEY METRICS
  Total Revenue        :    $157,432.18
  Average Order Value  :      $1,229.00
  Best Month           : Aug ($23,104.50)

TOP PRODUCTS BY QUANTITY SOLD
  1. Mouse        —  145 units
  2. Headphones   —   92 units
  3. Keyboard     —   78 units
  ...

MONTHLY REVENUE BREAKDOWN
  Jan   ████████████         $  14,320.00
  Feb   ███████████          $  13,980.00
  ...
```

### Charts
> After running the project, three PNG files appear in `charts/`:
> - `monthly_revenue.png` — Line chart of monthly revenue
> - `top_products.png`    — Horizontal bar chart of top products
> - `revenue_pie.png`     — Donut chart of revenue by product

---

## 🔮 Future Improvements

- [ ] Add a `config.yaml` to make file paths and settings configurable
- [ ] Support multi-year datasets with year-over-year comparison
- [ ] Export the summary report to a PDF
- [ ] Build an interactive dashboard using **Streamlit** or **Plotly Dash**
- [ ] Add unit tests with **pytest**
- [ ] Support additional input formats (Excel, JSON, SQLite)
- [ ] Add customer segmentation analysis (if customer data is available)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.
