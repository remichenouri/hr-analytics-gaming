import streamlit as st
import pandas as pd
import sys
import os
# Ajouts aux imports existants
from utils.helpers import load_css, format_number, create_gaming_themed_chart, display_gaming_easter_eggs
from data.gaming_data import UbisoftSpecificData, get_gaming_industry_stats

# Dans la fonction main(), après st.set_page_config
def main():
    # Charger le CSS personnalisé
    load_css("assets/style.css")
    
    # Easter eggs dans sidebar
    display_gaming_easter_eggs()
    
    # Stats industrie gaming
    gaming_stats = get_gaming_industry_stats()
    with st.sidebar.expander("📊 Gaming Industry Stats"):
        for key, value in gaming_stats.items():
            st.info(f"**{key.replace('_', ' ').title()}:** {value}")


# Ajout du chemin des modules
sys.path.append(os.path.dirname(__file__))

from data.data_generator import GamingIndustryDataGenerator
from components.workforce_insights import render_workforce_insights
from components.neurodiversity import render_neurodiversity_analysis
from components.retention_models import render_retention_models
from components.performance import render_performance_dashboard
from components.roi_calculator import render_roi_calculator

# Configuration de la page
st.set_page_config(
    page_title="Ubisoft People Analytics Demo",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 18px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def load_data():
    """Charge et cache les données simulées"""
    generator = GamingIndustryDataGenerator()
    
    data = {
        'workforce': generator.generate_workforce_data(),
        'neurodiversity': generator.generate_neurodiversity_data(),
        'retention': generator.generate_retention_data(),
        'roi': generator.generate_roi_data()
    }
    
    return data

@st.cache_data
def get_cached_data():
    return load_data()

def main():
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1>🎮 Ubisoft People Analytics Demo</h1>
        <p>Transforming Gaming Workforce Through Data-Driven Insights</p>
        <p><em>Created by Rémi CHENOURI - HR Data Analyst Candidate</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chargement des données
    with st.spinner("🔄 Loading gaming industry data..."):
        data = get_cached_data()
    
    # Sidebar avec informations
    with st.sidebar:
        st.image("https://via.placeholder.com/200x100/667eea/white?text=UBISOFT", width=200)
        
        st.markdown("""
        ### 🎯 Demo Features
        - **Real-time Analytics** - Live data simulation
        - **Predictive Models** - ML-powered insights  
        - **ROI Calculator** - Quantified business impact
        - **Gaming-Specific** - Industry-tailored metrics
        - **Neurodiversity Focus** - Inclusive workforce analytics
        """)
        
        st.markdown("""
        ### 📊 Data Sources
        - Simulated gaming industry benchmarks
        - Neurodiversity research findings
        - HR best practices from leading studios
        - Predictive modeling algorithms
        """)
        
        st.markdown("""
        ### 🚀 Technical Stack
        - **Python** - Data processing
        - **Streamlit** - Interactive dashboard
        - **Plotly** - Advanced visualizations
        - **Scikit-learn** - Machine learning
        - **Pandas** - Data manipulation
        """)
    
    # Onglets principaux
    tabs = st.tabs([
        "🎮 Workforce Insights", 
        "🧠 Neurodiversity Impact", 
        "📈 Retention Models",
        "🎯 Performance Dashboard",
        "💰 ROI Calculator"
    ])
    
    with tabs[0]:
        render_workforce_insights(data['workforce'])
    
    with tabs[1]:
        render_neurodiversity_analysis(data['neurodiversity'])
    
    with tabs[2]:
        render_retention_models(data['retention'])
    
    with tabs[3]:
        render_performance_dashboard()
    
    with tabs[4]:
        render_roi_calculator(data['roi'])
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>🎮 <strong>Ubisoft People Analytics Demo</strong> - Developed by Rémi CHENOURI</p>
        <p>💡 <em>Transforming gaming workforce through data-driven insights and inclusive analytics</em></p>
        <p>📧 chenouri.remi@proton.me | 🔗 linkedin.com/in/remi-chenouri</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()



