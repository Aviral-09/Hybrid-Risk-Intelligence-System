
import streamlit as st
import pandas as pd
import os

def apply_custom_css():

    st.markdown("""
    <style>

        html, body, [data-testid="stAppViewContainer"], .stApp {
            background-color: #FFF9E6 !important;
            color: #2C2C2C !important;
        }


        [data-testid="stSidebar"] {
            display: none !important;
            width: 0 !important;
        }
        
        [data-testid="collapsedControl"] {
            display: none !important;
        }
        

        .block-container {
            padding-top: 100px !important;
            padding-left: 5rem !important;
            padding-right: 5rem !important;
            max-width: 100% !important;
        }


        .top-nav {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 80px;
            background-color: #FFF3CC;
            border-bottom: 2px solid #E0D7B8;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 400px;
            z-index: 999999;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }

        .brand-text {
            font-weight: 800;
            color: #1F4E79;
            font-size: 1.4rem;
            letter-spacing: -0.5px;
        }


        div[data-testid="stMetric"], .stAlert, [data-testid="stTable"], [data-testid="stDataFrame"] {
            background-color: #FFFFFF !important;
            border: 1px solid #E0D7B8 !important;
            border-radius: 8px !important;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05) !important;
        }


        p, li, label, span, .stMarkdown, [data-testid="stWidgetLabel"] p {
            color: #2C2C2C !important;
        }

        h1, h2, h3, h4, h5, h6 {
            color: #1F4E79 !important;
            font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important;
            font-weight: 700 !important;
        }


        [data-testid="stMetricLabel"] {
            color: #5F6368 !important;
            font-weight: 700 !important;
        }
        [data-testid="stMetricValue"] {
            color: #1F4E79 !important;
        }


        .stButton button {
            background-color: #FFFFFF !important;
            border: 1px solid #E0D7B8 !important;
            color: #1F4E79 !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
        }
        .stButton button:hover {
            background-color: #FFF3CC !important;
            border-color: #1F4E79 !important;
        }


        .stSlider label, .stSelectbox label, .stTextInput label {
            color: #1F4E79 !important;
            font-weight: 700 !important;
        }


        .risk-high div[data-testid="stMetric"] { border-left: 8px solid #C62828 !important; }
        .risk-medium div[data-testid="stMetric"] { border-left: 8px solid #ED6C02 !important; }
        .risk-low div[data-testid="stMetric"] { border-left: 8px solid #2E7D32 !important; }


        .bg-card { background-color: #FFFFFF !important; border: 1px solid #E0D7B8 !important; border-radius: 8px; padding: 20px; }
        .bg-light-yellow { background-color: #FFF3CC !important; border: 1px solid #E0D7B8 !important; border-radius: 8px; padding: 20px; }


        header[data-testid="stHeader"] {
            display: none !important;
        }


        ::-webkit-scrollbar {
            width: 8px !important;
        }
        ::-webkit-scrollbar-track {
            background: #FFF9E6 !important;
        }
        ::-webkit-scrollbar-thumb {
            background: #E0D7B8 !important;
            border-radius: 10px !important;
        }
    </style>
    """, unsafe_allow_html=True)
    

    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        plt.rcParams.update({
            'figure.facecolor': '#FFF9E6',
            'axes.facecolor': '#FFFFFF',
            'grid.color': '#E6E6E6',
            'text.color': '#2C2C2C',
            'axes.labelcolor': '#2C2C2C',
            'xtick.color': '#444444', 
            'ytick.color': '#444444',
            'axes.edgecolor': '#5C5C5C',
            'axes.spines.top': False,
            'axes.spines.right': False,
            'legend.facecolor': '#FFFFFF',
            'legend.edgecolor': '#E0D7B8',
            'legend.framealpha': 0.8,
            'legend.labelcolor': '#2C2C2C'
        })
        sns.set_style("whitegrid", {
            'axes.facecolor': '#FFFFFF', 
            'figure.facecolor': '#FFF9E6',
            'axes.edgecolor': '#5C5C5C',
            'grid.color': '#E6E6E6'
        })
    except ImportError:
        pass

@st.cache_data
def load_data():
    base_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    try:
        credit = pd.read_csv(os.path.join(base_dir, 'credit_risk_scores.csv'))
        fraud = pd.read_csv(os.path.join(base_dir, 'fraud_risk_scores.csv'))
        hybrid = pd.read_csv(os.path.join(base_dir, 'hybrid_customer_profiles.csv'))
        return credit, fraud, hybrid
    except Exception:
        return None, None, None

def render_top_header():

    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = "Portal Home"


    st.markdown(f"""
        <div class="top-nav">
            <div style="display: flex; align-items: center; gap: 15px;">
                <span class="brand-text">HRIS PLATFORM</span>
            </div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="color: #2E7D32; font-weight: 700; font-size: 0.8rem; background: #E8F5E9; padding: 5px 12px; border-radius: 20px; border: 1px solid #C8E6C9;">SYSTEM OPERATIONAL</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    cols = st.columns([1, 1, 1, 1, 1])
    pages = [
        ("Portal Home", "Portal Home"),
        ("Executive Core", "Executive Core"),
        ("Credit Center", "Credit Center"),
        ("Fraud Scan", "Fraud Scan"),
        ("Hybrid Lab", "Hybrid Lab")
    ]

    for i, (label, value) in enumerate(pages):
        with cols[i]:

            is_selected = st.session_state['current_page'] == value
            btn_style = "border-bottom: 3px solid #1F4E79 !important;" if is_selected else ""
            if st.button(label, key=f"nav_{i}", use_container_width=True):
                st.session_state['current_page'] = value
                st.rerun()
    
    st.markdown("<hr style='margin-top:0; border: 0; border-top: 1px solid #E0D7B8;'>", unsafe_allow_html=True)
