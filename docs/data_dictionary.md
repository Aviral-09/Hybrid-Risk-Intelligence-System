
# Data Dictionary
**Project:** Hybrid Risk Intelligence System (HRIS)

## 1. Cleaned Credit Data (`cleaned_credit_data.csv`)
| Field | Type | Description |
|-------|------|-------------|
| `SeriousDlqin2yrs` | Integer | (Target) Person experienced 90 days past due delinquency or worse |
| `RevolvingUtilization...` | Float | Total balance on credit cards / credit limit |
| `age` | Integer | Age of borrower in years |
| `debt_to_income_ratio` | Float | Monthly debt payments / Monthly gross income |
| `MonthlyIncome` | Integer | Monthly income (Imputed median if missing) |
| `NumberOfOpenCredit...` | Integer | Number of open loans and credit lines |
| `LoanAmount` | Float | **(Simulated)** Estimated active loan amount for scoring |
| `emi_to_income_ratio` | Float | **(Derived)** Estimation of EMI burden relative to income |
| `risk_segment` | String | Initial risk categorization (High/Medium/Low) based on pre-scoring logic |
| `credit_risk_score` | Integer | **(Derived)** Final Rule-Based Risk Score (0-100) |
| `credit_risk_label` | String | Final Risk Category (High/Medium/Low) |

## 2. Cleaned Transaction Data (`cleaned_transaction_data.csv`)
| Field | Type | Description |
|-------|------|-------------|
| `Time` | Float | Seconds elapsed since first transaction in dataset |
| `Amount` | Float | Transaction amount |
| `Class` | Integer | (Target) 1 if Fraud, 0 if Legit (Original dataset label) |
| `transaction_hour` | Integer | **(Derived)** Hour of day (0-23) |
| `MerchantCategory` | String | **(Simulated)** Category of merchant (Grocery, Electronics, etc.) |
| `is_high_risk_merchant` | Integer | **(Derived)** 1 if Merchant Category is High Risk (e.g. Gambling) |
| `City` | String | **(Simulated)** Location of transaction |
| `transaction_velocity` | Integer | **(Derived)** Number of transactions by this user in that hour |
| `transaction_amount_zscore` | Float | **(Derived)** Std. Deviations from mean amount |
| `is_high_value` | Boolean | **(Flag)** True if Amount > 95th Percentile |
| `is_night_transaction` | Boolean | **(Flag)** True if Hour is 2, 3, or 4 |
| `fraud_risk_score` | Integer | **(Derived)** Final Rule-Based Fraud Score (0-100) |
| `fraud_risk_label` | String | Final Fraud Risk Category |

## 3. Hybrid Report (`hybrid_risk_report.csv`)
| Field | Type | Description |
|-------|------|-------------|
| `CustomerID` | Integer | Unique ID linking credit profile to transaction history |
| `credit_risk_score` | Integer | Max Credit Risk Score for customer |
| `fraud_risk_score` | Integer | Max Fraud Risk Score observed |
| `hybrid_risk_score` | Float | Average of Credit and Fraud scores |
| `hybrid_risk_status` | String | Combined assessment (Hypersensitive / Moderate / Standard) |
