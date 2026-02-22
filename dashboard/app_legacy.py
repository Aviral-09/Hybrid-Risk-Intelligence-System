
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import numpy as np


st.set_page_config(
    page_title="HRIS | Risk Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>

    .stApp {
        background-color: #0d1117;
        background-image: radial-gradient(at 50% 0%, #1f2937 0px, transparent 50%),
                          radial-gradient(at 100% 0%, #374151 0px, transparent 50%);
    }
    

    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 15px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        color: #e0e0e0;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
    

    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        color: #f3f4f6;
    }
    h1 {
        background: -webkit-linear-gradient(45deg, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    

    .js-plotly-plot .plotly .main-svg {
        background: rgba(0,0,0,0) !important;
    }
    

    section[data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    

    div[data-testid="stDataFrame"] {
        border: 1px solid #30363d;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    base_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    

    try:
        credit = pd.read_csv(os.path.join(base_dir, 'credit_risk_scores.csv'))
        fraud = pd.read_csv(os.path.join(base_dir, 'fraud_risk_scores.csv'))

        hybrid = pd.read_csv(os.path.join(base_dir, 'hybrid_customer_profiles.csv'))
        return credit, fraud, hybrid
    except FileNotFoundError:
        st.error("Data files not found. Please run the scripts first.")
        return None, None, None

credit_df, fraud_df, hybrid_df = load_data()


st.sidebar.title("HRIS System")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", ["Executive Overview", "Credit Risk Analytics", "Fraud Detection", "Hybrid Intelligence"])
st.sidebar.markdown("---")
st.sidebar.info("System Status: **Active**\n\nVersion: v2.1-Quant")


if page == "Executive Overview":
    st.title("Hybrid Risk Intelligence System")
    st.markdown("### Real-time Financial Risk Monitoring Console")
    

    col1, col2, col3, col4 = st.columns(4)
    
    total_customers = len(credit_df)
    high_risk_credit = len(credit_df[credit_df['risk_band'] == 'High Risk'])
    fraud_attempts = len(fraud_df[fraud_df['fraud_risk_score'] > 70])
    avg_hybrid_score = hybrid_df['hybrid_risk_score'].mean()
    
    col1.metric("Total Customers", f"{total_customers:,}", delta="+12%")
    col2.metric("High Risk Credit Profiles", f"{high_risk_credit:,}", delta="-2%", delta_color="inverse")
    col3.metric("Flagged Fraud Events", f"{fraud_attempts:,}", delta="+5%", delta_color="inverse")
    col4.metric("Avg Hybrid Risk Score", f"{avg_hybrid_score:.1f}", delta="Stable")
    
    st.markdown("---")
    

    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Credit Risk Distribution")
        fig_pie = px.pie(credit_df, names='risk_band', 
                         color='risk_band',
                         color_discrete_map={'High Risk':'#ef4444', 'Medium Risk':'#f59e0b', 'Low Risk':'#10b981'},
                         hole=0.6)
        fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with c2:
        st.subheader("Fraud Risk Trends (Last 24h)")

        fraud_trend = fraud_df.groupby('transaction_hour')['fraud_risk_score'].mean().reset_index()
        fig_line = px.area(fraud_trend, x='transaction_hour', y='fraud_risk_score',
                           color_discrete_sequence=['#f87171'])
        fig_line.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white",
                               xaxis_title="Hour of Day", yaxis_title="Avg Fraud Score")
        st.plotly_chart(fig_line, use_container_width=True)


elif page == "Credit Risk Analytics":
    st.title("Credit Risk Deep Dive")
    

    income_filter = st.slider("Filter by Monthly Income ($)", 0, 50000, (0, 50000))
    filtered_credit = credit_df[(credit_df['MonthlyIncome'] >= income_filter[0]) & 
                                (credit_df['MonthlyIncome'] <= income_filter[1])]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Debt-to-Income vs Risk Score")
        fig_scatter = px.scatter(filtered_credit.head(1000), 
                                 x='debt_to_income_ratio', y='credit_risk_score',
                                 color='risk_band',
                                 color_discrete_map={'High Risk':'#ef4444', 'Medium Risk':'#f59e0b', 'Low Risk':'#10b981'},
                                 size='LoanAmount',
                                 hover_data=['age', 'MonthlyIncome'])
        fig_scatter.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white",
                                  xaxis_range=[0, 2])
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    with col2:
        st.subheader("Risk Factors Breakdown")
        delinquency_counts = filtered_credit.groupby('risk_band')['SeriousDlqin2yrs'].sum().reset_index()
        fig_bar = px.bar(delinquency_counts, x='risk_band', y='SeriousDlqin2yrs',
                         color='risk_band',
                         color_discrete_map={'High Risk':'#ef4444', 'Medium Risk':'#f59e0b', 'Low Risk':'#10b981'})
        fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white", showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)
        st.caption("Count of borrowers with serious delinquency in last 2 years by Segment.")


elif page == "Fraud Detection":
    st.title("Transaction Anomaly Detection")
    st.markdown("Monitoring transaction velocity, amount outliers, and geo-inconsistencies.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Anomaly Heatmap: Hour vs Amount")

        sample_fraud = fraud_df.sample(2000)
        fig_heat = px.density_heatmap(sample_fraud, x='transaction_hour', y='Amount',
                                      nbinsx=24, nbinsy=20, color_continuous_scale='Magma')
        fig_heat.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig_heat, use_container_width=True)
        
    with col2:
        st.subheader("High Risk Merchants")
        merchant_risk = fraud_df[fraud_df['is_high_risk_merchant'] == 1]['MerchantCategory'].value_counts().reset_index()
        merchant_risk.columns = ['Category', 'Count']
        fig_donut = px.pie(merchant_risk, values='Count', names='Category', hole=0.7,
                           color_discrete_sequence=px.colors.sequential.Plasma)
        fig_donut.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig_donut, use_container_width=True)

    st.subheader("Suspicious Activity Log (High Score > 80)")
    suspicious = fraud_df[fraud_df['fraud_risk_score'] > 80][['Time', 'Amount', 'transaction_hour', 'MerchantCategory', 'City', 'fraud_risk_score', 'risk_reason_summary']]
    st.dataframe(suspicious.style.background_gradient(cmap='Reds', subset=['fraud_risk_score']), use_container_width=True)


elif page == "Hybrid Intelligence":
    st.title("Hybrid Customer View")
    st.markdown("Consolidated view of customers merging **Credit Health** and **Transaction Behavior**.")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Hypersensitive Customers", len(hybrid_df[hybrid_df['hybrid_risk_status'] == 'Hypersensitive']), "Requires Action")
    c2.metric("Moderate Risk", len(hybrid_df[hybrid_df['hybrid_risk_status'] == 'Moderate']))
    c3.metric("Safe Base", len(hybrid_df[hybrid_df['hybrid_risk_status'] == 'Standard']))
    
    st.markdown("### The Risk Matrix")
    

    size_col = 'txn_count_1h' if 'txn_count_1h' in hybrid_df.columns else 'transaction_velocity'
    

    fig_matrix = px.scatter(hybrid_df, x='credit_risk_score', y='fraud_risk_score',
                            color='hybrid_risk_status',
                            color_discrete_map={'Hypersensitive':'#ef4444', 'Moderate':'#f59e0b', 'Standard':'#10b981'},
                            size=size_col,
                            hover_data=['CustomerID'],
                            title="Credit Score vs. Fraud Score (Size = Velocity)")
    

    fig_matrix.add_vline(x=70, line_dash="dash", line_color="white", opacity=0.3)
    fig_matrix.add_hline(y=70, line_dash="dash", line_color="white", opacity=0.3)
    
    fig_matrix.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white",
                             xaxis_title="Credit Risk Score (0-100)",
                             yaxis_title="Fraud Risk Score (0-100)")
    
    st.plotly_chart(fig_matrix, use_container_width=True)
    
    st.markdown("### Hypersensitive Customers (Action List)")
    risky_customers = hybrid_df[hybrid_df['hybrid_risk_status'] == 'Hypersensitive'].sort_values(by='hybrid_risk_score', ascending=False)
    st.dataframe(risky_customers.head(50), use_container_width=True)

