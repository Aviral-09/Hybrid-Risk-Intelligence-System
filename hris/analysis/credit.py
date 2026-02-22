
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DATA_DIR = os.path.join(BASE_DIR, 'data')
PLOTS_DIR = os.path.join(BASE_DIR, 'plots')

def perform_credit_eda(df):

    print("Performing Credit Risk EDA...")
    if not os.path.exists(PLOTS_DIR):
        os.makedirs(PLOTS_DIR)

    plt.figure(figsize=(10, 6))
    sns.histplot(df['MonthlyIncome'], bins=50, kde=True)
    plt.title('Distribution of Monthly Income')
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

def generate_risk_segmentation(df):

    print("Generating Risk Segmentation...")
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
    
    summary.to_csv(os.path.join(DATA_DIR, 'credit_risk_segments_summary.csv'), index=False)
    return summary

def run_credit_analysis():
    CREDIT_CLEAN_PATH = os.path.join(DATA_DIR, 'cleaned_credit_data.csv')
    df = pd.read_csv(CREDIT_CLEAN_PATH)
    perform_credit_eda(df)
    generate_risk_segmentation(df)
    print("Credit analysis complete.")

if __name__ == "__main__":
    run_credit_analysis()
