# Customer-Churn-Revenue-Analytics

An end-to-end data analytics internship project using Python, SQL and Power BI.

## Project workflow

Raw data → Data quality → Cleaning → EDA → SQL → KPI validation → Dashboard → Report

## Folder structure

```text
customer_churn_analytics_project/
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   ├── data_quality.py
│   ├── data_cleaning.py
│   ├── eda.py
│   └── kpi_analysis.py
├── sql/
├── outputs/
│   ├── figures/
│   └── tables/
├── requirements.txt
└── README.md
```

## Setup

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the project

Put the real source CSV in:

```text
data/raw/customer_data.csv
```

Run data-quality profiling:

```bash
python src/data_quality.py --input data/raw/customer_data.csv
```

Create the processed dataset:

```bash
python src/data_cleaning.py --input data/raw/customer_data.csv --output data/processed/customer_data_clean.csv
```

Run EDA:

```bash
python src/eda.py --input data/processed/customer_data_clean.csv
```

Generate KPI table:

```bash
python src/kpi_analysis.py --input data/processed/customer_data_clean.csv
```

## Responsible analysis

Do not replace measured results with assumed values. Keep the raw dataset separate from processed data, document every cleaning rule, and validate important KPIs across Python, SQL and the dashboard.

The exact column names may differ across datasets. Update the scripts only after inspecting the real dataset and record those changes in the project report.
