
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from hris.core.engine import compute_transaction_risk_score


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DATA_DIR = os.path.join(BASE_DIR, 'data')
PLOTS_DIR = os.path.join(BASE_DIR, 'plots')

def run_backtesting():

    print("Running Backtesting Simulation...")
    
    FRAUD_CLEAN_PATH = os.path.join(DATA_DIR, 'cleaned_transaction_data.csv')
    df = pd.read_csv(FRAUD_CLEAN_PATH)
    

    scored_df = compute_transaction_risk_score(df)
    
    if 'datetime' not in scored_df.columns:
         scored_df['datetime'] = pd.to_datetime(scored_df['Time'], unit='s', origin='2024-01-01')

    scored_df['Month'] = scored_df['datetime'].dt.to_period('M')
    
    monthly_stats = scored_df.groupby('Month').agg({
        'fraud_risk_score': ['mean', 'count'],
        'risk_band': lambda x: (x == 'High Risk').sum()
    }).reset_index()
    
    monthly_stats.columns = ['Month', 'Avg_Risk_Score', 'Total_Txns', 'High_Risk_Flags']
    monthly_stats['Flag_Rate_Pct'] = (monthly_stats['High_Risk_Flags'] / monthly_stats['Total_Txns']) * 100
    
    monthly_stats.to_csv(os.path.join(DATA_DIR, 'backtest_summary.csv'), index=False)
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=monthly_stats, x=monthly_stats['Month'].astype(str), y='Flag_Rate_Pct', marker='o')
    plt.title('Monthly High Risk Flag Rate')
    plt.ylabel('Flag Rate (%)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, 'backtest_trend.png'))
    print("Backtesting complete.")

if __name__ == "__main__":
    run_backtesting()
