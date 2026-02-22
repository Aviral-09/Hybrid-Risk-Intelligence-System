
# Hybrid Risk Intelligence System (HRIS) - Rule-Based Credit Risk & Fraud Analytics

## Project Overview
The **Hybrid Risk Intelligence System (HRIS)** is a production-quality data analysis project designed to assess financial risk without relying on "Black Box" Machine Learning models. Instead, it utilizes **audit-proof rule-based logic**, statistical thresholds, and exploratory data analysis to flag high-risk customers and fraudulent transactions.

This system demonstrates how traditional financial analytics, combined with modern data engineering, can provide transparent and explainable risk scoring for banking institutions.

## Problem Statement
Financial institutions face two critical risks:
1.  **Credit Risk**: Customers defaulting on loans.
2.  **Fraud Risk**: Unauthorized or anomalous transactions.

While ML models are popular, they often lack interpretability. This project builds a transparent **Rule-Based Scoring Engine** to detect these risks using strictly defined business rules and statistical anomalies.

## Tools & Technologies
-   **Python**: Core logic and data processing.
-   **Pandas/NumPy**: Data cleaning, manipulation, and vectorization.
-   **Seaborn/Matplotlib**: Financial visualizations and heatmaps.
-   **Rule-Based Logic**: Deterministic scoring algorithms.

## Project Structure
```
/data                   # Raw & Cleaned Datasets (Credit and Transaction logs)
/scripts
    ├── data_cleaning.py                # Missing value imputation, outlier removal
    ├── credit_risk_analysis.py         # EDA, Segmentation, Distribution Plots
    ├── transaction_anomaly_research.py # Anomaly detection (Time, Geo, Velocity)
    ├── risk_engine.py                  # Quant-Style Risk Scoring Engine (Profiling & Vectorized)
    ├── backtesting_engine.py           # Historical rule application simulator
    └── hybrid_dashboard_prep.py        # Generates Reports for Dashboards
/dashboard
    └── app.py                          # Streamlit Interactive Dashboard (Dark Glass UI)
/plots                  # Generated Visualizations
/docs                   # Documentation (Insights, Data Dictionary)
```

## Summary of Rule-Based Scoring

### A) Credit Risk Score (0-100)
A cumulative score based on financial health:
-   **+25 Points**: DTI > 80th Percentile (High Debt burden)
-   **+25 Points**: EMI/Income > 80th Percentile
-   **+20 Points**: No Credit History
-   **+10 Points**: Low Income (< 10th Percentile)
-   **+10 Points**: High Loan Amount (> 75th percentile)

**Risk Bands:** High (≥70), Medium (40-69), Low (<40).

### B) Fraud Risk Score (0-100)
A simplified anomaly detection score:
-   **+15 Points**: High Value (> 95th percentile)
-   **+20 Points**: Extreme Value (> 99th percentile)
-   **+15 Points**: Velocity Spike (> 99th percentile hourly)
-   **+25 Points**: Burst Activity (> 99.5th percentile 5-min)
-   **+10 Points**: Night Transaction (2 AM - 4 AM)
-   **+15 Points**: High Risk Merchant Category
-   **+35 Points**: Geo-Inconsistency (Impossible Travel)

## Key Methodology: Why Rule-Based?
This project deliberately chooses a **Deterministic Rule-Based Architecture** over Probabilistic ML for:
1.  **Zero-Hallucination**: No statistical guesses. Flags are absolute.
2.  **Instant Auditing**: Regulators can see exactly *why* a customer was flagged (e.g., "High DTI + Velocity Spike").
3.  **Performance**: Vectorized Pandas operations allow processing millions of rows in seconds.

## How to Run
1.  Install dependencies: `pip install pandas numpy seaborn matplotlib`
2.  Run the pipeline:
    ```bash
    python scripts/data_cleaning.py
    python scripts/credit_risk_analysis.py
    python scripts/transaction_anomaly_research.py
    python scripts/risk_engine.py
    python scripts/backtesting_engine.py
    python scripts/hybrid_dashboard_prep.py
    ```

3.  **Launch the Interactive Dashboard**:
    This project includes a modern "Dark Glass" style dashboard built with Streamlit and Plotly.
    ```bash
    pip install streamlit plotly
    streamlit run dashboard/app.py
    ```

---
