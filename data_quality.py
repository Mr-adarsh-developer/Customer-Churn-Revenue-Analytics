"""
Data Quality Assessment
Project: Customer Churn & Revenue Analytics

Purpose:
    Profile a raw customer dataset before any business analysis.
    The script does not silently modify the raw file.

Usage:
    python src/data_quality.py --input data/raw/customer_data.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd


def profile_dataset(df: pd.DataFrame) -> dict:
    """Return reproducible, high-level data-quality metrics."""
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_cells": int(df.isna().sum().sum()),
        "columns_with_missing": int((df.isna().sum() > 0).sum()),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to raw CSV file")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    df = pd.read_csv(input_path)

    print("\n=== DATASET PROFILE ===")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns):,}")
    print(f"Duplicate rows: {df.duplicated().sum():,}")
    print(f"Missing cells: {df.isna().sum().sum():,}")

    print("\n=== COLUMN TYPES ===")
    print(df.dtypes.to_string())

    print("\n=== MISSING VALUES ===")
    missing = (
        df.isna()
        .sum()
        .sort_values(ascending=False)
        .rename("missing_count")
    )
    missing_pct = (missing / len(df) * 100).round(2).rename("missing_pct")
    quality = pd.concat([missing, missing_pct], axis=1)
    print(quality[quality["missing_count"] > 0].to_string())

    print("\n=== NUMERIC SUMMARY ===")
    print(df.describe(include="number").T.to_string())

    print("\n=== CATEGORICAL SUMMARY ===")
    print(df.describe(include="object").T.to_string())

    print("\n=== PROFILE DICTIONARY ===")
    print(profile_dataset(df))


if __name__ == "__main__":
    main()
