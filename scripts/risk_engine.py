
import pandas as pd
import numpy as np
import os
import time
from functools import wraps


DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
CREDIT_CLEAN_PATH = os.path.join(DATA_DIR, 'cleaned_credit_data.csv')
FRAUD_CLEAN_PATH = os.path.join(DATA_DIR, 'cleaned_transaction_data.csv')
CREDIT_SCORES_PATH = os.path.join(DATA_DIR, 'credit_risk_scores.csv')
FRAUD_SCORES_PATH = os.path.join(DATA_DIR, 'fraud_risk_scores.csv')

def profile_runtime(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"[{func.__name__}] Execution Time: {end_time - start_time:.4f} seconds")
        return result
    return wrapper

@profile_runtime
def compute_credit_risk_score(df):

    print("Computing Credit Risk Scores...")
    

    df['credit_risk_score'] = 0
    df['risk_reason_summary'] = ""
    

    dti_thresh = df['debt_to_income_ratio'].quantile(0.80)
    mask_dti = df['debt_to_income_ratio'] > dti_thresh
    df.loc[mask_dti, 'credit_risk_score'] += 25
    df.loc[mask_dti, 'risk_reason_summary'] += "High DTI; "
    

    emi_thresh = df['emi_to_income_ratio'].quantile(0.80)
    mask_emi = df['emi_to_income_ratio'] > emi_thresh
    df.loc[mask_emi, 'credit_risk_score'] += 25
    df.loc[mask_emi, 'risk_reason_summary'] += "High EMI Burden; "
    

    no_history = (df['NumberOfOpenCreditLinesAndLoans'] == 0) & (df['NumberRealEstateLoansOrLines'] == 0)
    df.loc[no_history, 'credit_risk_score'] += 20
    df.loc[no_history, 'risk_reason_summary'] += "No Credit History; "
    

    income_thresh = df['MonthlyIncome'].quantile(0.10)
    mask_income = df['MonthlyIncome'] < income_thresh
    df.loc[mask_income, 'credit_risk_score'] += 10
    df.loc[mask_income, 'risk_reason_summary'] += "Low Income; "
    

    high_loan_thresh = df['LoanAmount'].quantile(0.75)
    mask_loan = df['LoanAmount'] > high_loan_thresh
    df.loc[mask_loan, 'credit_risk_score'] += 10
    df.loc[mask_loan, 'risk_reason_summary'] += "Large Loan Request; "
    

    df['credit_risk_score'] = df['credit_risk_score'].clip(upper=100)
    

    conditions = [
        (df['credit_risk_score'] >= 70),
        (df['credit_risk_score'] >= 40)
    ]
    choices = ['High Risk', 'Medium Risk']
    df['risk_band'] = np.select(conditions, choices, default='Low Risk')
    
    return df

@profile_runtime
def compute_transaction_risk_score(df):

    print("Computing Transaction Risk Scores...")
    

    df['fraud_risk_score'] = 0
    df['risk_reason_summary'] = ""
    


    df['datetime'] = pd.to_datetime(df['Time'], unit='s', origin='2024-01-01')
    df = df.sort_values(by=['CustomerID', 'datetime'])
    


    df_indexed = df.set_index('datetime')
    grouped = df_indexed.groupby('CustomerID')['Amount']
    

    df['txn_count_5min'] = grouped.rolling('5min').count().values
    


    df['txn_count_1h'] = grouped.rolling('1h').count().values





    thresh_95 = df['Amount'].quantile(0.95)
    thresh_99 = df['Amount'].quantile(0.99)
    
    mask_99 = df['Amount'] > thresh_99
    df.loc[mask_99, 'fraud_risk_score'] += 20
    df.loc[mask_99, 'risk_reason_summary'] += "Extreme Price Shock (>99th%); "
    
    mask_95_all = df['Amount'] > thresh_95
    df.loc[mask_95_all, 'fraud_risk_score'] += 15
    df.loc[mask_95_all, 'risk_reason_summary'] += "High Value (>95th%); "
    
    mask_99_add = df['Amount'] > thresh_99
    df.loc[mask_99_add, 'fraud_risk_score'] += 5
    df.loc[mask_99_add, 'risk_reason_summary'] += "Extreme Value (>99th%); "
    

    burst_thresh = df['txn_count_5min'].quantile(0.995) 
    velocity_thresh = df['txn_count_1h'].quantile(0.99)
    
    burst_thresh = max(burst_thresh, 5)
    velocity_thresh = max(velocity_thresh, 10)
    
    mask_burst = df['txn_count_5min'] > burst_thresh
    df.loc[mask_burst, 'fraud_risk_score'] += 25
    df.loc[mask_burst, 'risk_reason_summary'] += f"Burst Activity; "
    
    mask_velocity = df['txn_count_1h'] > velocity_thresh
    df.loc[mask_velocity, 'fraud_risk_score'] += 15
    df.loc[mask_velocity, 'risk_reason_summary'] += f"High Velocity; "


    mask_night = df['transaction_hour'].isin([2, 3, 4])
    df.loc[mask_night, 'fraud_risk_score'] += 10
    df.loc[mask_night, 'risk_reason_summary'] += "Illiquid Hours; "
    


    if 'is_high_risk_merchant' in df.columns:
        mask_merchant = df['is_high_risk_merchant'] == 1
        df.loc[mask_merchant, 'fraud_risk_score'] += 15
        df.loc[mask_merchant, 'risk_reason_summary'] += "High Risk Merchant; "
    


    prev_city = df.groupby('CustomerID')['City'].shift(1)
    prev_time = df.groupby('CustomerID')['Time'].shift(1)
    
    geo_inconsistency = (
        (df['City'] != prev_city) & 
        (pd.notnull(prev_city)) &
        ((df['Time'] - prev_time) <= 3600)
    )
    df.loc[geo_inconsistency, 'fraud_risk_score'] += 35
    df.loc[geo_inconsistency, 'risk_reason_summary'] += "Impossible Travel; "
    

    df['fraud_risk_score'] = df['fraud_risk_score'].clip(upper=100)
    

    conditions = [
        (df['fraud_risk_score'] >= 70),
        (df['fraud_risk_score'] >= 40)
    ]
    choices = ['High Risk', 'Medium Risk']
    df['risk_band'] = np.select(conditions, choices, default='Low Risk')
    
    return df

def main():

    credit_df = pd.read_csv(CREDIT_CLEAN_PATH)
    fraud_df = pd.read_csv(FRAUD_CLEAN_PATH)
    

    credit_scored = compute_credit_risk_score(credit_df)
    fraud_scored = compute_transaction_risk_score(fraud_df)
    

    print(f"Saving scores to {DATA_DIR}...")
    credit_scored.to_csv(CREDIT_SCORES_PATH, index=False)
    fraud_scored.to_csv(FRAUD_SCORES_PATH, index=False)
    print("Risk Engine Execution Complete.")

if __name__ == "__main__":
    main()
