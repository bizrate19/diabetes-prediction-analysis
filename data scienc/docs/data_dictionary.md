# Data Dictionary

## Overview
This document describes the dataset used for the customer analysis project.

## Table: `customers`

| Column Name | Data Type | Description | Notes |
|-------------|-----------|-------------|-------|
| customer_id | string | Unique identifier for each customer | Primary key, format: CUST-XXXXX |
| signup_date | date | Date when customer created account | YYYY-MM-DD format |
| age | integer | Customer's age in years | Values range: 18-100 |
| country | string | Customer's country of residence | ISO country codes |
| subscription_tier | string | Current subscription plan | Values: 'Basic', 'Premium', 'Enterprise' |
| monthly_spend | decimal | Amount spent in last 30 days | In USD, 2 decimal places |
| last_login | datetime | Most recent login timestamp | UTC timezone |
| activity_score | integer | Customer engagement metric | Scale: 0-100 |
| churn_risk | boolean | Flag for churn prediction | True = High risk, False = Low risk |

## Table: `transactions`

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| transaction_id | string | Unique transaction identifier |
| customer_id | string | References customers.customer_id |
| transaction_date | date | Date of transaction |
| amount | decimal | Transaction value |
| product_category | string | Category of purchased product |