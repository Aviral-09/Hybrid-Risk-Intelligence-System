
import pandas as pd
import numpy as np
import os
from hris.utils.profiling import profile_runtime


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DATA_DIR = os.path.join(BASE_DIR, 'data')

@profile_runtime
def generate_hybrid_report():
    print("Generating Hybrid Risk Report...")
    
    CREDIT_SCORES_PATH = os.path.join(DATA_DIR, 'credit_risk_scores.csv')
    FRAUD_SCORES_PATH = os.path.join(DATA_DIR, 'fraud_risk_scores.csv')
    
    credit_df = pd.read_csv(CREDIT_SCORES_PATH)
    fraud_df = pd.read_csv(FRAUD_SCORES_PATH)
    

    np.random.seed(42)
    credit_df['CustomerID'] = np.random.randint(1000, 6000, size=len(credit_df))
    credit_agg = credit_df.groupby('CustomerID').agg({
        'credit_risk_score': 'max',
        'risk_band': 'first',
        'MonthlyIncome': 'mean'
    }).reset_index()
    

    fraud_agg = fraud_df.groupby('CustomerID').agg({
        'fraud_risk_score': 'max',
        'risk_band': 'first',
        'txn_count_1h': 'mean' 
    }).reset_index()
    
    fraud_agg.rename(columns={'risk_band': 'fraud_risk_band'}, inplace=True)
    credit_agg.rename(columns={'risk_band': 'credit_risk_band'}, inplace=True)
    

    hybrid_df = pd.merge(credit_agg, fraud_agg, on='CustomerID', how='inner')
    

    hybrid_df['hybrid_risk_score'] = (hybrid_df['credit_risk_score'] + hybrid_df['fraud_risk_score']) / 2
    
    conditions = [
        (hybrid_df['hybrid_risk_score'] >= 70),
        (hybrid_df['hybrid_risk_score'] >= 40)
    ]
    choices = ['Hypersensitive', 'Moderate']
    hybrid_df['hybrid_risk_status'] = np.select(conditions, choices, default='Standard')
    

    total_customers = len(hybrid_df)
    high_risk_count = (hybrid_df['hybrid_risk_status'] == 'Hypersensitive').sum()
    high_risk_pct = (high_risk_count / total_customers) * 100 if total_customers > 0 else 0
    review_reduction_pct = 100 - high_risk_pct
    

    detailed_path = os.path.join(DATA_DIR, 'hybrid_customer_profiles.csv')
    hybrid_df.to_csv(detailed_path, index=False)
    
    summary_data = {
        'Metric': ['Total Customers', 'High Risk Count', 'High Risk %', 'Manual Review Reduction %'],
        'Value': [total_customers, high_risk_count, f"{high_risk_pct:.2f}%", f"{review_reduction_pct:.2f}%"]
    }
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_csv(os.path.join(DATA_DIR, 'hybrid_risk_report.csv'), index=False)
    print("Hybrid report generated.")

if __name__ == "__main__":
    generate_hybrid_report()
