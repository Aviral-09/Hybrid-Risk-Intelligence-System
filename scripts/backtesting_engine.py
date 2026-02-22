
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from risk_engine import compute_transaction_risk_score, FRAUD_CLEAN_PATH, DATA_DIR

BACKTEST_SUMMARY_PATH = os.path.join(DATA_DIR, 'backtest_summary.csv')
TIME_SERIES_PLOT_PATH = os.path.join(DATA_DIR, '../plots/backtest_trend.png')

def run_backtest():

    print("Running Backtesting Simulation...")
    

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
    
    print("\nBacktest Results (Monthly):")
    print(monthly_stats)
    

    monthly_stats.to_csv(BACKTEST_SUMMARY_PATH, index=False)
    print(f"Backtest summary saved to {BACKTEST_SUMMARY_PATH}")
    

    if not os.path.exists(os.path.dirname(TIME_SERIES_PLOT_PATH)):
        os.makedirs(os.path.dirname(TIME_SERIES_PLOT_PATH))
        
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=monthly_stats, x=monthly_stats['Month'].astype(str), y='Flag_Rate_Pct', marker='o')
    plt.title('Monthly High Risk Flag Rate')
    plt.ylabel('Flag Rate (%)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(TIME_SERIES_PLOT_PATH)
    print(f"Backtest trend plot saved to {TIME_SERIES_PLOT_PATH}")

if __name__ == "__main__":
    run_backtest()
