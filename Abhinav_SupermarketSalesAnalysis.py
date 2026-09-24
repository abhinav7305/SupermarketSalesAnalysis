"""Supermarket Sales Analysis - IBM SkillsBuild Data Analytics project."""

from __future__ import annotations
import argparse
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

PROJECT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_DIR / "outputs"
DEFAULT_FILENAMES = ("supermarket_sales - Sheet1.csv", "supermarket_sales.csv",
                     "data/supermarket_sales - Sheet1.csv", "data/supermarket_sales.csv")

def find_data_file(path_argument: str | None) -> Path:
    if path_argument:
        path = Path(path_argument)
        if path.is_file():
            return path
        raise FileNotFoundError(f"Dataset not found: {path}")
    for filename in DEFAULT_FILENAMES:
        path = PROJECT_DIR / filename
        if path.is_file():
            return path
    raise FileNotFoundError("Dataset not found. Download it from Kaggle; pass --data or save it in the project root/data folder.")

def clean_data(csv_path: Path) -> pd.DataFrame:
    """Load, validate, de-duplicate, and standardize Kaggle source data."""
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()
    required = {"Branch", "City", "Customer type", "Product line", "Unit price", "Quantity", "Payment", "Rating"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required column(s): {', '.join(sorted(missing))}")
    df = df.drop_duplicates().copy()
    for column in ("Unit price", "Quantity", "Rating"):
        df[column] = pd.to_numeric(df[column], errors="coerce")
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Sales"] = df["Quantity"] * df["Unit price"]
    return df

def save_bar_chart(series: pd.Series, title: str, xlabel: str, filename: str) -> None:
    values = series.sort_values(ascending=False)
    # A branch/city summary has a pandas MultiIndex. Convert each index entry
    # individually so both ordinary and multi-level summaries can be plotted.
    labels = [" - ".join(map(str, item)) if isinstance(item, tuple) else str(item)
              for item in values.index]
    plt.figure(figsize=(10, 5.5))
    ax = sns.barplot(x=values.values, y=labels, hue=labels,
                     palette="viridis", legend=False)
    ax.set(title=title, xlabel=xlabel, ylabel="")
    for container in ax.containers:
        ax.bar_label(container, fmt="%.0f", padding=3, fontsize=8)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / filename, dpi=200, bbox_inches="tight")
    plt.close()

def analyse(df: pd.DataFrame) -> dict[str, pd.Series | float]:
    """Aggregate the project questions and create tables and charts."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    sns.set_theme(style="whitegrid", palette="deep")
    product_sales = df.groupby("Product line")["Sales"].sum().sort_values(ascending=False)
    branch_sales = df.groupby(["Branch", "City"])["Sales"].sum().sort_values(ascending=False)
    payment_counts = df["Payment"].value_counts()
    customer_average = df.groupby("Customer type")["Sales"].mean().sort_values(ascending=False)
    average_rating = float(df["Rating"].mean())
    product_sales.rename("Sales").to_csv(OUTPUT_DIR / "sales_by_product_line.csv")
    branch_sales.rename("Sales").to_csv(OUTPUT_DIR / "sales_by_branch.csv")
    payment_counts.rename("Transactions").to_csv(OUTPUT_DIR / "payment_method_counts.csv")
    customer_average.rename("Average sales").to_csv(OUTPUT_DIR / "customer_type_average_sales.csv")
    pd.DataFrame({"Metric": ["Rows", "Columns", "Missing values", "Invalid sales rows"],
                  "Value": [len(df), len(df.columns), int(df.isna().sum().sum()), int(df["Sales"].isna().sum())]}).to_csv(OUTPUT_DIR / "data_quality_summary.csv", index=False)
    save_bar_chart(product_sales, "Sales by Product Line", "Sales (Quantity x Unit Price)", "01_sales_by_product_line.png")
    save_bar_chart(branch_sales, "Sales by Branch and City", "Sales (Quantity x Unit Price)", "02_sales_by_branch.png")
    save_bar_chart(payment_counts, "Payment Method Popularity", "Transactions", "03_payment_methods.png")
    save_bar_chart(customer_average, "Average Transaction Value by Customer Type", "Average Sales", "04_customer_type_average.png")
    return {"product_sales": product_sales, "branch_sales": branch_sales, "payment_counts": payment_counts, "customer_average": customer_average, "average_rating": average_rating}

def render_summary(results: dict[str, pd.Series | float], source_rows: int, clean_rows: int) -> str:
    product_sales, branch_sales = results["product_sales"], results["branch_sales"]
    payment_counts, customer_average = results["payment_counts"], results["customer_average"]
    product, product_value = product_sales.index[0], float(product_sales.iloc[0])
    (branch, city), branch_value = branch_sales.index[0], float(branch_sales.iloc[0])
    payment, payment_count = payment_counts.index[0], int(payment_counts.iloc[0])
    member, normal = float(customer_average.get("Member", float("nan"))), float(customer_average.get("Normal", float("nan")))
    rating = float(results["average_rating"])
    higher = "Members" if member > normal else "Normal customers"
    return f"""SUPERMARKET SALES ANALYSIS - RESULTS
Source rows: {source_rows}; rows after duplicate removal: {clean_rows}

1. Highest-revenue product line: {product} ({product_value:,.2f})
2. Best-performing branch: Branch {branch}, {city} ({branch_value:,.2f})
3. Highest-selling category: {product} ({product_value:,.2f})
4. Most-used payment method: {payment} ({payment_count} transactions)
5. Average Member transaction: {member:,.2f}
6. Average Normal transaction: {normal:,.2f}
   Higher-spending group: {higher}
7. Average customer rating: {rating:.2f} out of 10

Sales is calculated as Quantity x Unit price. The Kaggle Total column includes tax and is not substituted for this project measure.
"""

def main() -> None:
    parser = argparse.ArgumentParser(description="Analyse Kaggle supermarket sales data.")
    parser.add_argument("--data", help="Path to the downloaded Kaggle CSV file.")
    args = parser.parse_args()
    data_path = find_data_file(args.data)
    source_rows = len(pd.read_csv(data_path))
    df = clean_data(data_path)
    summary = render_summary(analyse(df), source_rows, len(df))
    (OUTPUT_DIR / "analysis_summary.txt").write_text(summary, encoding="utf-8")
    print(summary)
    print(f"Tables, charts, and the summary were saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
