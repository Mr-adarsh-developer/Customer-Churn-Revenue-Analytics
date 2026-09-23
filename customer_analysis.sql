-- Customer Churn & Revenue Analytics
-- Run these queries after importing the processed dataset into your database.
-- Adjust identifiers/types to match your database engine.

-- 1. Total customers
SELECT COUNT(*) AS total_customers
FROM customers;

-- 2. Churned customers
SELECT COUNT(*) AS churned_customers
FROM customers
WHERE Churn = 'Yes';

-- 3. Churn by contract
SELECT
    Contract,
    COUNT(*) AS customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(
        100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS churn_rate_pct
FROM customers
GROUP BY Contract
ORDER BY churn_rate_pct DESC;

-- 4. Revenue by contract
SELECT
    Contract,
    SUM(TotalCharges) AS total_recorded_charges,
    AVG(TotalCharges) AS average_recorded_charges
FROM customers
GROUP BY Contract
ORDER BY total_recorded_charges DESC;

-- 5. Average monthly charges by churn status
SELECT
    Churn,
    AVG(MonthlyCharges) AS average_monthly_charges
FROM customers
GROUP BY Churn;

-- 6. Customer count by payment method and churn
SELECT
    PaymentMethod,
    Churn,
    COUNT(*) AS customers
FROM customers
GROUP BY PaymentMethod, Churn
ORDER BY PaymentMethod, Churn;
