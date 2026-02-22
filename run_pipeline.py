
import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from hris.core.cleaning import run_cleaning_pipeline
from hris.core.engine import run_scoring_engine
from hris.analysis.credit import run_credit_analysis
from hris.analysis.fraud import run_fraud_analysis
from hris.research.backtesting import run_backtesting
from hris.reporting.dashboard_prep import generate_hybrid_report

def main():
    print("=== HRIS System Execution Started ===")
    

    run_cleaning_pipeline()
    

    run_credit_analysis()
    run_fraud_analysis()
    

    run_scoring_engine()
    

    run_backtesting()
    

    generate_hybrid_report()
    
    print("=== HRIS System Execution Completed Successfully ===")

if __name__ == "__main__":
    main()
