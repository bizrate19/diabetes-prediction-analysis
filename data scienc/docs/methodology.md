# Project Methodology

## 1. Project Overview
**Project:** Customer Segmentation and Churn Analysis  
**Objective:** Identify customer segments and predict churn risk to improve retention strategies.  
**Time Period:** Data from January 2023 - March 2024

## 2. Data Collection
- **Source:** Production database export
- **Tables Used:** `customers`, `transactions`, `user_sessions`
- **Extraction Date:** 2024-05-27
- **Tool:** SQL queries via company data warehouse

## 3. Data Cleaning Process

### 3.1 Handling Missing Values
- Removed 12 records with null `customer_id` (0.1% of dataset)
- Imputed missing `age` values with median (32 years)
- Filled missing `country` with 'Unknown' category

### 3.2 Data Validation
- Corrected 45 records with negative `monthly_spend` values
- Standardized `subscription_tier` categories (merged 'Pro' into 'Premium')
- Removed duplicate customer records (7 instances)

### 3.3 Data Transformation
- Created `customer_tenure` feature: `today() - signup_date`
- Calculated `avg_monthly_spend`: Rolling 3-month average
- Created `login_frequency`: Logins per week average

## 4. Feature Engineering

### 4.1 Behavioral Features
- `engagement_score`: Composite metric of login frequency and session duration
- `spending_trend`: Slope of spending over last 6 months
- `product_diversity`: Count of unique product categories purchased

### 4.2 Technical Features
- Normalized numerical features using StandardScaler
- One-hot encoded categorical variables (`country`, `subscription_tier`)
- Created interaction term: `tenure * monthly_spend`

## 5. Analytical Methods

### 5.1 Customer Segmentation
- **Algorithm:** K-means Clustering
- **Features used:** `monthly_spend`, `engagement_score`, `tenure`
- **Optimal clusters:** 4 (determined by elbow method)

### 5.2 Churn Prediction
- **Algorithm:** Random Forest Classifier
- **Target variable:** `churn_risk`
- **Evaluation metric:** F1-score (achieved 0.87)
- **Train-test split:** 80-20 with stratified sampling

## 6. Tools & Technologies
- **Programming:** Python 3.9
- **Libraries:** Pandas, Scikit-learn, Matplotlib, Seaborn
- **Environment:** Jupyter Notebook, Git version control