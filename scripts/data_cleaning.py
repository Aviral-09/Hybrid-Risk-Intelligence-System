
import pandas as pd
import numpy as np
import os


DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
CREDIT_RAW_PATH = os.path.join(DATA_DIR, 'credit_risk_train.csv')
FRAUD_RAW_PATH = os.path.join(DATA_DIR, 'creditcard.csv')
CREDIT_CLEAN_PATH = os.path.join(DATA_DIR, 'cleaned_credit_data.csv')
FRAUD_CLEAN_PATH = os.path.join(DATA_DIR, 'cleaned_transaction_data.csv')

def load_data(path):

    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    return pd.read_csv(path)

def clean_credit_data(df):

    print("Cleaning Credit Data...")
    


    df['MonthlyIncome'] = df['MonthlyIncome'].fillna(df['MonthlyIncome'].median())

    df['NumberOfDependents'] = df['NumberOfDependents'].fillna(0)
    


    df = df[df['age'] > 18].copy()
    

    cap_debt = df['DebtRatio'].quantile(0.99)
    df['DebtRatio'] = np.where(df['DebtRatio'] > cap_debt, cap_debt, df['DebtRatio'])
    

    np.random.seed(42)
    

    df['LoanAmount'] = df['MonthlyIncome'] * np.random.uniform(5, 20, size=len(df))

    df['LoanAmount'] = df['LoanAmount'].apply(lambda x: max(1000, round(x, -2)))
    

    df['TotalMonthlyDebt'] = df['MonthlyIncome'] * df['DebtRatio']
    

    df['emi_to_income_ratio'] = df['DebtRatio']
    

    df.rename(columns={'DebtRatio': 'debt_to_income_ratio'}, inplace=True)
    


    df['MonthlyIncome'] = df['MonthlyIncome'].astype(int)
    
    print(f"Credit Data Cleaned: {df.shape}")
    return df

def clean_fraud_data(df):

    print("Cleaning Fraud Data...")
    

    df['transaction_hour'] = (df['Time'] // 3600) % 24
    

    np.random.seed(42)
    n = len(df)
    

    categories = ['Grocery', 'Electronics', 'Jewelry', 'Gambling', 'Utilities', 'Travel']
    weights = [0.4, 0.2, 0.1, 0.05, 0.15, 0.1]
    df['MerchantCategory'] = np.random.choice(categories, size=n, p=weights)
    

    high_risk_cats = ['Gambling', 'Jewelry', 'Electronics']
    df['is_high_risk_merchant'] = df['MerchantCategory'].apply(lambda x: 1 if x in high_risk_cats else 0)
    

    cities = ['New York', 'London', 'Paris', 'Tokyo', 'Mumbai', 'Sydney', 'Berlin', 'Toronto']
    df['City'] = np.random.choice(cities, size=n)
    

    

    mean_amt = df['Amount'].mean()
    std_amt = df['Amount'].std()
    df['transaction_amount_zscore'] = (df['Amount'] - mean_amt) / std_amt
    

    df['CustomerID'] = np.random.randint(1000, 6000, size=n)
    


    df['relative_day'] = df['Time'] // 86400
    velocity = df.groupby(['CustomerID', 'relative_day', 'transaction_hour']).size().reset_index(name='transaction_velocity')
    df = df.merge(velocity, on=['CustomerID', 'relative_day', 'transaction_hour'], how='left')
    
    print(f"Fraud Data Cleaned: {df.shape}")
    return df

def main():

    print("Loading datasets...")

    credit_df = load_data(CREDIT_RAW_PATH)
    fraud_df = load_data(FRAUD_RAW_PATH)
    

    credit_clean = clean_credit_data(credit_df)
    fraud_clean = clean_fraud_data(fraud_df)
    

    print(f"Saving cleaned data to {DATA_DIR}...")
    credit_clean.to_csv(CREDIT_CLEAN_PATH, index=False)
    fraud_clean.to_csv(FRAUD_CLEAN_PATH, index=False)
    print("Data Cleaning Complete.")

if __name__ == "__main__":
    main()
