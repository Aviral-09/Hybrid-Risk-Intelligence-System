
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from hris.utils.profiling import profile_runtime


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DATA_DIR = os.path.join(BASE_DIR, 'data')
PLOTS_DIR = os.path.join(BASE_DIR, 'plots')

@profile_runtime
def analyze_transaction_anomalies(df):

    print("Performing Transaction Anomaly Analysis...")
    if not os.path.exists(PLOTS_DIR):
        os.makedirs(PLOTS_DIR)

    threshold_95 = df['Amount'].quantile(0.95)
    df['is_high_value'] = df['Amount'] > threshold_95
    
    plot_df = df.sample(min(10000, len(df)))
    plt.figure(figsize=(10, 6))
    plt.scatter(plot_df['transaction_hour'], plot_df['Amount'], 
                c=plot_df['Class'], cmap='coolwarm', alpha=0.5)
    plt.title('Transaction Amount vs Hour (Colored by Fraud Class)')
    plt.savefig(os.path.join(PLOTS_DIR, 'fraud_heatmap_amount_hour.png'))
    plt.close()
    
    df['is_night_transaction'] = df['transaction_hour'].between(2, 4)
    
    plt.figure(figsize=(10, 6))
    sns.countplot(y='MerchantCategory', data=df, hue='is_high_risk_merchant', palette='viridis')
    plt.title('Distribution of Transactions by Merchant Category')
    plt.savefig(os.path.join(PLOTS_DIR, 'fraud_merchant_distribution.png'))
    plt.close()

@profile_runtime
def generate_anomaly_summary(df):

    suspicious = df[(df['is_high_value']) & (df['is_night_transaction'])]
    summary_path = os.path.join(DATA_DIR, 'suspicious_transactions_summary.csv')
    suspicious[['Time', 'Amount', 'transaction_hour', 'MerchantCategory', 'City']].head(100).to_csv(summary_path, index=False)
    print(f"Summary saved to {summary_path}")

def run_fraud_analysis():
    FRAUD_CLEAN_PATH = os.path.join(DATA_DIR, 'cleaned_transaction_data.csv')
    df = pd.read_csv(FRAUD_CLEAN_PATH)
    analyze_transaction_anomalies(df)
    generate_anomaly_summary(df)
    print("Fraud analysis complete.")

if __name__ == "__main__":
    run_fraud_analysis()
