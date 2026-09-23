"""
Exploratory Data Analysis
Project: Customer Churn & Revenue Analytics

This script creates reproducible tables and figures from the processed
dataset. It checks for expected columns before running each analysis.

Usage:
    python src/eda.py --input data/processed/customer_data_clean.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def first_existing(df: pd.DataFrame, candidates: list[str]) -> str | None:
    for col in candidates:
        if col in df.columns:
            return col
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", default="outputs")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    figures_dir = output_dir / "figures"
    tables_dir = output_dir / "tables"
    figures_dir.mkdir(parents=True, exist_ok=True)
    tables_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)

    churn_col = first_existing(df, ["Churn", "churn"])
    contract_col = first_existing(df, ["Contract", "contract"])
    monthly_col = first_existing(df, ["MonthlyCharges", "monthly_charges"])
    total_col = first_existing(df, ["TotalCharges", "total_charges"])
    tenure_col = first_existing(df, ["tenure", "Tenure"])

    sns.set_theme()

    # Overall churn distribution.
    if churn_col:
        counts = df[churn_col].value_counts(dropna=False)
        counts.to_csv(tables_dir / "churn_counts.csv")

        plt.figure(figsize=(7, 5))
        sns.countplot(data=df, x=churn_col)
        plt.title("Customer Churn Distribution")
        plt.xlabel("Churn Status")
        plt.ylabel("Number of Customers")
        plt.tight_layout()
        plt.savefig(figures_dir / "churn_distribution.png", dpi=200)
        plt.close()

    # Churn by contract.
    if churn_col and contract_col:
        cross = pd.crosstab(
            df[contract_col],
            df[churn_col],
            normalize="index"
        ).mul(100).round(2)
        cross.to_csv(tables_dir / "churn_by_contract_pct.csv")

        plt.figure(figsize=(9, 5))
        sns.countplot(data=df, x=contract_col, hue=churn_col)
        plt.title("Customer Churn by Contract Type")
        plt.xlabel("Contract Type")
        plt.ylabel("Number of Customers")
        plt.xticks(rotation=20)
        plt.tight_layout()
        plt.savefig(figures_dir / "churn_by_contract.png", dpi=200)
        plt.close()

    # Monthly charges by churn.
    if churn_col and monthly_col:
        df[monthly_col] = pd.to_numeric(df[monthly_col], errors="coerce")

        summary = (
            df.groupby(churn_col)[monthly_col]
            .agg(["count", "mean", "median", "min", "max"])
            .round(2)
        )
        summary.to_csv(tables_dir / "monthly_charges_by_churn.csv")

        plt.figure(figsize=(8, 5))
        sns.boxplot(data=df, x=churn_col, y=monthly_col)
        plt.title("Monthly Charges by Churn Status")
        plt.xlabel("Churn Status")
        plt.ylabel("Monthly Charges")
        plt.tight_layout()
        plt.savefig(figures_dir / "monthly_charges_by_churn.png", dpi=200)
        plt.close()

    # Total charges by contract.
    if contract_col and total_col:
        df[total_col] = pd.to_numeric(df[total_col], errors="coerce")
        revenue = (
            df.groupby(contract_col)[total_col]
            .agg(["count", "sum", "mean", "median"])
            .round(2)
        )
        revenue.to_csv(tables_dir / "revenue_by_contract.csv")

    # Tenure distribution.
    if tenure_col:
        df[tenure_col] = pd.to_numeric(df[tenure_col], errors="coerce")
        plt.figure(figsize=(8, 5))
        sns.histplot(df[tenure_col].dropna(), bins=20, kde=True)
        plt.title("Customer Tenure Distribution")
        plt.xlabel("Tenure")
        plt.ylabel("Number of Customers")
        plt.tight_layout()
        plt.savefig(figures_dir / "tenure_distribution.png", dpi=200)
        plt.close()

    print(f"EDA outputs saved under: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
