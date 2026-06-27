import sys
import os

import streamlit as st
import pandas as pd

sys.path.append(os.path.dirname(__file__))

from data.data_generator import GamingIndustryDataGenerator
from components.workforce_insights import render_workforce_insights
from components.neurodiversity import render_neurodiversity_analysis
from components.retention_models import render_retention_models
from components.performance import render_performance_dashboard
from components.roi_calculator import render_roi_calculator

PRIMARY = "#17867A"

st.set_page_config(
    page_title="Gaming Industry People Analytics",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(f"""
<style>
    .main-header {{
        background: linear-gradient(90deg, {PRIMARY} 0%, #0f5c52 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }}
    .metric-card {{
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid {PRIMARY};
    }}
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {{
        font-size: 16px;
        font-weight: 600;
    }}
</style>
""", unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def get_cached_data() -> dict:
    """Generate and cache all synthetic datasets for the session."""
    generator = GamingIndustryDataGenerator()
    return {
        "workforce": generator.generate_workforce_data(),
        "neurodiversity": generator.generate_neurodiversity_data(),
        "retention": generator.generate_retention_data(),
        "roi": generator.generate_roi_data(),
    }


def main() -> None:
    """Entry point for the Streamlit dashboard."""
    st.markdown("""
    <div class="main-header">
        <h1>🎮 Gaming Industry People Analytics</h1>
        <p>Workforce Planning &amp; Diversity KPIs — Portfolio Case Study</p>
        <p><em>All data is synthetic · Not affiliated with any company</em></p>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Loading synthetic dataset…"):
        data = get_cached_data()

    with st.sidebar:
        st.markdown(f"### 🎯 Dashboard Modules")
        st.markdown("""
        - **Workforce Insights** — headcount & turnover trends
        - **Neurodiversity Impact** — inclusion & innovation KPIs
        - **Retention Models** — ML-powered churn prediction
        - **Performance Dashboard** — team & individual KPIs
        - **ROI Calculator** — cost-of-attrition & program returns
        """)

        st.markdown("### 📊 Data")
        st.markdown("""
        - Synthetic gaming-industry benchmarks
        - Reproducible random seed (42)
        - ~1 000 employee records
        """)

        st.markdown("### 🛠 Tech Stack")
        st.markdown("""
        `Python` · `Streamlit` · `Plotly` · `scikit-learn` · `pandas`
        """)

    tabs = st.tabs([
        "🎮 Workforce Insights",
        "🧠 Neurodiversity Impact",
        "📈 Retention Models",
        "🎯 Performance Dashboard",
        "💰 ROI Calculator",
    ])

    with tabs[0]:
        render_workforce_insights(data["workforce"])

    with tabs[1]:
        render_neurodiversity_analysis(data["neurodiversity"])

    with tabs[2]:
        render_retention_models(data["retention"])

    with tabs[3]:
        render_performance_dashboard()

    with tabs[4]:
        render_roi_calculator(data["roi"])

    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; color:#666; padding:1.5rem;">
        <p>🎮 <strong>Gaming Industry People Analytics</strong> — Portfolio project by Rémi Chenouri</p>
        <p><em>Synthetic data only · Not affiliated with any gaming company</em></p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
