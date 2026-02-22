
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
PLOTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'plots'))
CREDIT_CLEAN_PATH = os.path.join(DATA_DIR, 'cleaned_credit_data.csv')

def load_data():
    return pd.read_csv(CREDIT_CLEAN_PATH)

def perform_eda(df):

    print("Performing Credit Risk EDA...")
    

    plt.figure(figsize=(10, 6))
    sns.histplot(df['MonthlyIncome'], bins=50, kde=True)
    plt.title('Distribution of Monthly Income')
    plt.xlabel('Monthly Income')
    plt.grid(True)
    plt.savefig(os.path.join(PLOTS_DIR, 'credit_income_distribution.png'))
    plt.close()
    

    plt.figure(figsize=(10, 6))
    sns.histplot(df[df['debt_to_income_ratio'] < 2]['debt_to_income_ratio'], bins=50, kde=True)
    plt.title('Debt-to-Income Ratio Distribution (Zoomed < 2.0)')
    plt.savefig(os.path.join(PLOTS_DIR, 'credit_dti_distribution.png'))
    plt.close()
    

    plt.figure(figsize=(12, 10))

    cols = ['SeriousDlqin2yrs', 'age', 'debt_to_income_ratio', 'MonthlyIncome', 
            'NumberOfOpenCreditLinesAndLoans', 'NumberRealEstateLoansOrLines', 'LoanAmount']
    corr = df[cols].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Credit Risk Correlation Heatmap')
    plt.savefig(os.path.join(PLOTS_DIR, 'credit_correlation_heatmap.png'))
    plt.close()
    

    plt.figure(figsize=(10, 6))
    sns.histplot(df['LoanAmount'], bins=50, kde=True, color='green')
    plt.title('Simulated Loan Amount Distribution')
    plt.savefig(os.path.join(PLOTS_DIR, 'credit_loanamount_distribution.png'))
    plt.close()
    
def generate_risk_tables(df):

    print("Generating Risk Tables...")
    

    conditions = [
        (df['SeriousDlqin2yrs'] == 1),
        (df['debt_to_income_ratio'] > 0.6) | (df['NumberOfTimes90DaysLate'] > 0),
        (df['MonthlyIncome'] > 5000) & (df['debt_to_income_ratio'] < 0.3)
    ]
    choices = ['High Risk (Delinquent)', 'Medium Risk (High DTI/Late)', 'Low Risk (Prime)']
    df['risk_segment'] = np.select(conditions, choices, default='Medium Risk')
    

    summary = df.groupby('risk_segment').agg({
        'MonthlyIncome': 'mean',
        'debt_to_income_ratio': 'mean',
        'age': 'mean',
        'LoanAmount': 'mean',
        'SeriousDlqin2yrs': 'count'
    }).rename(columns={'SeriousDlqin2yrs': 'Count'}).reset_index()
    
    print("\nRisk Segmentation Summary:")
    print(summary)
    

    summary.to_csv(os.path.join(DATA_DIR, 'credit_risk_segments_summary.csv'), index=False)
    
import numpy as np

def main():
    if not os.path.exists(PLOTS_DIR):
        os.makedirs(PLOTS_DIR)
        
    df = load_data()
    perform_eda(df)
    generate_risk_tables(df)
    print("Credit Risk Analysis Complete. Plots saved to /plots.")

if __name__ == "__main__":
    main()
