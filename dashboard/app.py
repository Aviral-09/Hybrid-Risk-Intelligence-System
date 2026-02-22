import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
from utils import apply_custom_css, load_data, render_top_header


st.set_page_config(
    page_title="HRIS | Institutional Portal",
    layout="wide",
    initial_sidebar_state="collapsed"
)


apply_custom_css()


def update_chart_layout(fig):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='#FFFFFF',
        font=dict(color='#2C2C2C'),
        xaxis=dict(
            gridcolor='#E6E6E6', 
            zerolinecolor='#E6E6E6',
            showline=True,
            linecolor='#5C5C5C',
            tickcolor='#444444',
            tickfont=dict(color='#2C2C2C')
        ),
        yaxis=dict(
            gridcolor='#E6E6E6', 
            zerolinecolor='#E6E6E6',
            showline=True,
            linecolor='#5C5C5C',
            tickcolor='#444444',
            tickfont=dict(color='#2C2C2C')
        ),
        legend=dict(
            font=dict(color='#2C2C2C'),
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='#E0D7B8',
            borderwidth=1
        ),
        margin=dict(l=20, r=20, t=40, b=20),
        template="plotly_white"
    )
    return fig



def render_executive_core(credit_df, fraud_df, hybrid_df):
    st.title("Executive Intelligence Dashboard")
    st.markdown("Global Systemic Risk Analysis & Monitoring")
    
    col1, col2, col3, col4 = st.columns(4)
    total_customers = len(credit_df)
    high_risk_credit = len(credit_df[credit_df['risk_band'] == 'High Risk'])
    fraud_attempts = len(fraud_df[fraud_df['fraud_risk_score'] > 70])
    avg_hybrid_score = hybrid_df['hybrid_risk_score'].mean()
    
    with col1:
        st.markdown('<div class="risk-low">', unsafe_allow_html=True)
        st.metric("Total Customers", f"{total_customers:,}", delta="+1.2%")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="risk-high">', unsafe_allow_html=True)
        st.metric("High Risk Credit Profiles", f"{high_risk_credit:,}", delta="-2%", delta_color="inverse")
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="risk-high">', unsafe_allow_html=True)
        st.metric("Flagged Fraud Events", f"{fraud_attempts:,}", delta="+5%", delta_color="inverse")
        st.markdown('</div>', unsafe_allow_html=True)
    with col4:
        risk_class = "risk-low" if avg_hybrid_score < 40 else "risk-medium" if avg_hybrid_score < 70 else "risk-high"
        st.markdown(f'<div class="{risk_class}">', unsafe_allow_html=True)
        st.metric("Avg Hybrid Risk Score", f"{avg_hybrid_score:.1f}", delta="Stable")
        st.markdown('</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Credit Risk Distribution")
        fig_pie = px.pie(credit_df, names='risk_band', color='risk_band',
                         color_discrete_map={'High Risk':'#C62828', 'Medium Risk':'#ED6C02', 'Low Risk':'#2E7D32'},
                         hole=0.6)
        st.plotly_chart(update_chart_layout(fig_pie), use_container_width=True)
    with c2:
        st.subheader("Fraud Risk Trends (Last 24h)")
        fraud_trend = fraud_df.groupby('transaction_hour')['fraud_risk_score'].mean().reset_index()
        fig_line = px.area(fraud_trend, x='transaction_hour', y='fraud_risk_score', color_discrete_sequence=['#C62828'])
        st.plotly_chart(update_chart_layout(fig_line), use_container_width=True)

def render_credit_center(credit_df):
    st.title("Credit Risk Assessment")
    st.markdown("Detailed exposure analysis and borrower delinquency profiling.")
    st.markdown('<div class="bg-light-yellow">', unsafe_allow_html=True)
    income_filter = st.slider("Filter by Monthly Income ($)", 0, 50000, (0, 50000))
    st.markdown('</div>', unsafe_allow_html=True)
    
    filtered_credit = credit_df[(credit_df['MonthlyIncome'] >= income_filter[0]) & (credit_df['MonthlyIncome'] <= income_filter[1])]
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Debt-to-Income vs. Risk Quantization")
        fig_scatter = px.scatter(filtered_credit.head(1000), x='debt_to_income_ratio', y='credit_risk_score',
                                 color='risk_band', size='LoanAmount',
                                 color_discrete_map={'High Risk':'#C62828', 'Medium Risk':'#ED6C02', 'Low Risk':'#2E7D32'})
        fig_scatter.update_layout(xaxis_range=[0, 2])
        st.plotly_chart(update_chart_layout(fig_scatter), use_container_width=True)
    with col2:
        st.subheader("Delinquency Vectors")
        delinquency_counts = filtered_credit.groupby('risk_band')['SeriousDlqin2yrs'].sum().reset_index()
        fig_bar = px.bar(delinquency_counts, x='risk_band', y='SeriousDlqin2yrs', color='risk_band',
                         color_discrete_map={'High Risk':'#C62828', 'Medium Risk':'#ED6C02', 'Low Risk':'#2E7D32'})
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(update_chart_layout(fig_bar), use_container_width=True)

def render_fraud_scan(fraud_df):
    st.title("Fraud Surveillance System")
    st.markdown("Automated monitoring of transaction velocity and geospatial anomalies.")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Anomaly Heatmap")
        fig_heat = px.density_heatmap(fraud_df.sample(min(2000, len(fraud_df))), x='transaction_hour', y='Amount',
                                      nbinsx=24, nbinsy=20, color_continuous_scale='Blues')
        st.plotly_chart(update_chart_layout(fig_heat), use_container_width=True)
    with col2:
        st.subheader("High Risk Merchants")
        merchant_risk = fraud_df[fraud_df['is_high_risk_merchant'] == 1]['MerchantCategory'].value_counts().reset_index()
        merchant_risk.columns = ['Category', 'Count']
        fig_donut = px.pie(merchant_risk, values='Count', names='Category', hole=0.7)
        st.plotly_chart(update_chart_layout(fig_donut), use_container_width=True)
    
    st.subheader("Surveillance Registry")
    suspicious = fraud_df[fraud_df['fraud_risk_score'] > 80][['Time', 'Amount', 'MerchantCategory', 'fraud_risk_score']]
    st.dataframe(suspicious.style.background_gradient(cmap='YlOrRd', subset=['fraud_risk_score']), use_container_width=True)

def render_hybrid_lab(hybrid_df):
    st.title("Strategic Risk Synthesis")
    st.markdown("Consolidated multi-vector intelligence merging Credit and Transaction data.")
    st.markdown("### Integrated Risk Matrix")
    fig_matrix = px.scatter(hybrid_df, x='credit_risk_score', y='fraud_risk_score', color='hybrid_risk_status',
                            color_discrete_map={'Hypersensitive':'#C62828', 'Moderate':'#ED6C02', 'Standard':'#2E7D32'},
                            size='hybrid_risk_score')
    fig_matrix.add_vline(x=70, line_dash="dash", line_color="#C62828", opacity=0.3)
    fig_matrix.add_hline(y=70, line_dash="dash", line_color="#C62828", opacity=0.3)
    st.plotly_chart(update_chart_layout(fig_matrix), use_container_width=True)

def render_portal_home(credit_df, fraud_df, hybrid_df):
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #FFF3CC 0%, #FFFFFF 100%); border: 1px solid #E2D7B8; padding: 40px; border-radius: 12px; margin-bottom: 30px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);">
            <h1 style="margin:0; color: #1F4E79;">Institutional Command Center</h1>
            <p style="color: #5F6368; font-size: 1.1rem; margin-top: 10px; font-weight: 500;">
                Hybrid Risk Intelligence System &middot; Version 2.2.0-Production &middot; {datetime.date.today().strftime('%B %d, %Y')}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Key Risk Indicators")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="risk-low">', unsafe_allow_html=True)
        st.metric("Portfolio Coverage", f"{len(credit_df):,}", "Active Nodes")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        fraud_val = len(fraud_df[fraud_df['fraud_risk_score'] > 75])
        st.markdown('<div class="risk-high">', unsafe_allow_html=True)
        st.metric("Critical Anomalies", f"{fraud_val:,}", "High Severity")
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        hybrid_avg = hybrid_df['hybrid_risk_score'].mean()
        risk_class = "risk-low" if hybrid_avg < 40 else "risk-medium" if hybrid_avg < 70 else "risk-high"
        st.markdown(f'<div class="{risk_class}">', unsafe_allow_html=True)
        st.metric("Global Risk Posture", f"{hybrid_avg:.2f}", "Stability Index")
        st.markdown('</div>', unsafe_allow_html=True)


def main():
    credit_df, fraud_df, hybrid_df = load_data()
    render_top_header()
    
    if credit_df is None or fraud_df is None or hybrid_df is None:
        st.warning("Please run the data pipeline to generate risk scores before accessing the dashboard.")
        st.info("Locally: Run 'python run_pipeline.py'. In cloud: Ensure data files are pushed to the repository.")
        st.stop()
        
    page_selection = st.session_state.get('current_page', "Portal Home")
    
    with st.container():
        if page_selection == "Portal Home":
            render_portal_home(credit_df, fraud_df, hybrid_df)
        elif page_selection == "Executive Core":
            render_executive_core(credit_df, fraud_df, hybrid_df)
        elif page_selection == "Credit Center":
            render_credit_center(credit_df)
        elif page_selection == "Fraud Scan":
            render_fraud_scan(fraud_df)
        elif page_selection == "Hybrid Lab":
            render_hybrid_lab(hybrid_df)

if __name__ == "__main__":
    main()
