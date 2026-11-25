"""Create sample datasets. Run from the backend folder:
    python scripts/generate_sample_data.py          (small files)
    python scripts/generate_sample_data.py --all    (also 100k and 1M row files)
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parents[2] / "sample_data"

REGIONS = ["North", "South", "East", "West", "Central"]
PRODUCTS = {
    "Laptop": "Electronics", "Phone": "Electronics",
    "Desk": "Furniture", "Chair": "Furniture",
    "Notebook": "Stationery", "Pen": "Stationery",
}


def make_sales(n, seed=42):
    rng = np.random.default_rng(seed)
    products = rng.choice(list(PRODUCTS.keys()), n)
    df = pd.DataFrame({
        "order_id": np.arange(1, n + 1),
        "order_date": pd.to_datetime("2024-01-01") + pd.to_timedelta(rng.integers(0, 365, n), unit="D"),
        "region": rng.choice(REGIONS, n),
        "product": products,
        "category": [PRODUCTS[p] for p in products],
        "customer_id": rng.integers(1000, 1000 + max(n // 10, 50), n),
        "quantity": rng.integers(1, 10, n),
        "unit_price": np.round(rng.uniform(5, 1500, n), 2),
    })
    df["revenue"] = np.round(df["quantity"] * df["unit_price"], 2)
    df["discount"] = np.round(rng.uniform(0, 0.3, n), 2)
    df.loc[rng.random(n) < 0.05, "discount"] = np.nan  # about 5% missing
    dupes = df.sample(frac=0.01, random_state=seed)     # about 1% duplicates
    return pd.concat([df, dupes], ignore_index=True)


def make_employees(n, seed=7):
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "employee_id": np.arange(1, n + 1),
        "department": rng.choice(["Engineering", "Sales", "HR", "Finance", "Support"], n),
        "city": rng.choice(["Hyderabad", "Bengaluru", "Chennai", "Pune"], n),
        "age": rng.integers(21, 60, n),
        "years_experience": rng.integers(0, 30, n),
        "salary": np.round(rng.normal(70000, 20000, n), 0),
    })
    df.loc[rng.random(n) < 0.08, "salary"] = np.nan
    dupes = df.sample(frac=0.02, random_state=seed)
    return pd.concat([df, dupes], ignore_index=True)


def main():
    OUT.mkdir(exist_ok=True)
    make_sales(1000).to_csv(OUT / "sales_small.csv", index=False)
    make_employees(300).to_csv(OUT / "employees.csv", index=False)
    if "--all" in sys.argv:
        make_sales(100000).to_csv(OUT / "sales_medium.csv", index=False)
        make_sales(1000000).to_csv(OUT / "sales_large.csv", index=False)
    print("Sample data written to", OUT)


if __name__ == "__main__":
    main()
