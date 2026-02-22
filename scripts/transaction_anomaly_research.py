
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
import time
from functools import wraps

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
PLOTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'plots'))
FRAUD_CLEAN_PATH = os.path.join(DATA_DIR, 'cleaned_transaction_data.csv')

def profile_runtime(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"[{func.__name__}] Execution Time: {end_time - start_time:.4f} seconds")
        return result
    return wrapper

def load_data():
    return pd.read_csv(FRAUD_CLEAN_PATH)

@profile_runtime
def analyze_transaction_anomalies(df):

    print("Performing Transaction Anomaly Analysis...")
    

    threshold_95 = df['Amount'].quantile(0.95)
    df['is_high_value'] = df['Amount'] > threshold_95
    print(f"High Value Threshold (95th%): {threshold_95:.2f}")
    

    plot_df = df.sample(min(10000, len(df)))
    plt.figure(figsize=(10, 6))
    plt.scatter(plot_df['transaction_hour'], plot_df['Amount'], 
                c=plot_df['Class'], cmap='coolwarm', alpha=0.5, label='Fraud/Legit')
    plt.title('Transaction Amount vs Hour (Colored by Fraud Class)')
    plt.xlabel('Hour of Day')
    plt.ylabel('Transaction Amount')
    plt.colorbar(label='Class (1=Fraud)')
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(PLOTS_DIR, 'fraud_heatmap_amount_hour.png'))
    plt.close()
    

    df['is_night_transaction'] = df['transaction_hour'].between(2, 4)
    
    night_fraud_rate = df[df['is_night_transaction']]['Class'].mean() * 100
    day_fraud_rate = df[~df['is_night_transaction']]['Class'].mean() * 100
    print(f"Fraud Rate (2-4 AM): {night_fraud_rate:.4f}% vs Normal Hours: {day_fraud_rate:.4f}%")
    

    plt.figure(figsize=(10, 6))
    sns.countplot(y='MerchantCategory', data=df, hue='is_high_risk_merchant', palette='viridis')
    plt.title('Distribution of Transactions by Merchant Category')
    plt.savefig(os.path.join(PLOTS_DIR, 'fraud_merchant_distribution.png'))
    plt.close()
    

    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Class', y='Amount', data=df)
    plt.title('Transaction Amount Distribution by Class (Log Scale)')
    plt.yscale('log')
    plt.savefig(os.path.join(PLOTS_DIR, 'fraud_amount_boxplot.png'))
    plt.close()

@profile_runtime
def generate_anomaly_summary(df):


    suspicious = df[(df['is_high_value']) & (df['is_night_transaction'])]
    
    summary_path = os.path.join(DATA_DIR, 'suspicious_transactions_summary.csv')
    suspicious[['Time', 'Amount', 'transaction_hour', 'MerchantCategory', 'City']].head(100).to_csv(summary_path, index=False)
    print(f"Suspicious transactions summary saved to {summary_path}")

def main():
    if not os.path.exists(PLOTS_DIR):
        os.makedirs(PLOTS_DIR)
        
    df = load_data()
    analyze_transaction_anomalies(df)
    generate_anomaly_summary(df)
    print("Transaction Anomaly Analysis Complete. Plots saved to /plots.")

if __name__ == "__main__":
    main()
