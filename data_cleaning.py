"""
Data Cleaning Pipeline
Project: Customer Churn & Revenue Analytics

The cleaning rules are deliberately explicit. Adjust them only after
reviewing the actual dataset and documenting the decision in the report.

Usage:
    python src/data_cleaning.py \
        --input data/raw/customer_data.csv \
        --output data/processed/customer_data_clean.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd


def clean_customer_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize a customer churn dataset."""
    data = df.copy()

    # Standardize column names.
    data.columns = (
        data.columns.astype(str)
        .str.strip()
        .str.replace(" ", "_", regex=False)
    )

    # Remove exact duplicate records.
    data = data.drop_duplicates().copy()

    # Convert common numeric fields when they exist.
    for col in ["tenure", "Tenure", "MonthlyCharges", "monthly_charges",
                "TotalCharges", "total_charges"]:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")

    # Standardize text fields without changing their business meaning.
    text_columns = data.select_dtypes(include="object").columns
    for col in text_columns:
        data[col] = data[col].astype("string").str.strip()

    # Normalize common churn labels if the column exists.
    for col in ["Churn", "churn"]:
        if col in data.columns:
            data[col] = data[col].replace(
                {
                    "Yes": "Yes",
                    "No": "No",
                    "yes": "Yes",
                    "no": "No",
                    "Y": "Yes",
                    "N": "No",
                }
            )

    # Create a tenure group only when tenure is available.
    tenure_col = "tenure" if "tenure" in data.columns else "Tenure" if "Tenure" in data.columns else None
    if tenure_col:
        data["TenureGroup"] = pd.cut(
            data[tenure_col],
            bins=[-1, 12, 24, 48, 72, float("inf")],
            labels=["0-12", "13-24", "25-48", "49-72", "73+"],
        )

    return data


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    df = pd.read_csv(input_path)
    cleaned = clean_customer_data(df)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(output_path, index=False)

    print("Cleaning completed.")
    print(f"Input rows : {len(df):,}")
    print(f"Output rows: {len(cleaned):,}")
    print(f"Output file: {output_path}")


if __name__ == "__main__":
    main()
