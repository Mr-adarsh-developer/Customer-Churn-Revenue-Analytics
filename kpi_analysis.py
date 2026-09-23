"""
KPI Analysis
Project: Customer Churn & Revenue Analytics

Produces a small, auditable KPI table from the processed dataset.
It does not invent values: missing columns result in an explicit
'N/A' rather than a guessed metric.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="outputs/tables/kpis.csv")
    args = parser.parse_args()

    df = pd.read_csv(args.input)

    churn_col = "Churn" if "Churn" in df.columns else "churn" if "churn" in df.columns else None
    monthly_col = "MonthlyCharges" if "MonthlyCharges" in df.columns else "monthly_charges" if "monthly_charges" in df.columns else None
    total_col = "TotalCharges" if "TotalCharges" in df.columns else "total_charges" if "total_charges" in df.columns else None
    tenure_col = "tenure" if "tenure" in df.columns else "Tenure" if "Tenure" in df.columns else None

    total_customers = len(df)
    churned = None
    churn_rate = None

    if churn_col:
        normalized = df[churn_col].astype("string").str.strip().str.lower()
        churned = int((normalized == "yes").sum())
        churn_rate = round(churned / total_customers * 100, 2) if total_customers else None

    if monthly_col:
        df[monthly_col] = pd.to_numeric(df[monthly_col], errors="coerce")
        avg_monthly = round(df[monthly_col].mean(), 2)
    else:
        avg_monthly = None

    if total_col:
        df[total_col] = pd.to_numeric(df[total_col], errors="coerce")
        total_revenue = round(df[total_col].sum(), 2)
    else:
        total_revenue = None

    if tenure_col:
        df[tenure_col] = pd.to_numeric(df[tenure_col], errors="coerce")
        avg_tenure = round(df[tenure_col].mean(), 2)
    else:
        avg_tenure = None

    result = pd.DataFrame(
        [
            ["Total Customers", total_customers],
            ["Churned Customers", churned],
            ["Observed Churn Rate (%)", churn_rate],
            ["Total Recorded Charges", total_revenue],
            ["Average Monthly Charges", avg_monthly],
            ["Average Tenure", avg_tenure],
        ],
        columns=["KPI", "Value"],
    )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output, index=False)

    print(result.to_string(index=False))
    print(f"\nSaved: {output}")


if __name__ == "__main__":
    main()
