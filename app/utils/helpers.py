"""
Fonctions utilitaires pour l'application Ubisoft People Analytics
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import base64

def load_css(file_path):
    """Charge et applique un fichier CSS à l'application Streamlit"""
    try:
        with open(file_path) as f:
            css_content = f.read()
        
        st.markdown(f"""
        <style>
        {css_content}
        </style>
        """, unsafe_allow_html=True)
        
        return True
    except FileNotFoundError:
        st.warning(f"⚠️ CSS file not found: {file_path}")
        return False
    except Exception as e:
        st.error(f"❌ Error loading CSS: {str(e)}")
        return False

def format_number(number, prefix="", suffix=""):
    """Formate les nombres avec séparateurs et préfixes/suffixes"""
    if pd.isna(number):
        return "N/A"
    
    if abs(number) >= 1e9:
        formatted = f"{number/1e9:.1f}B"
    elif abs(number) >= 1e6:
        formatted = f"{number/1e6:.1f}M"
    elif abs(number) >= 1e3:
        formatted = f"{number/1e3:.1f}K"
    else:
        formatted = f"{number:,.0f}" if number == int(number) else f"{number:,.1f}"
    
    return f"{prefix}{formatted}{suffix}"

def create_metric_card(title, value, delta=None, delta_color="normal"):
    """Crée une carte métrique stylisée"""
    delta_html = ""
    if delta is not None:
        color = "green" if delta_color == "normal" and "+" in str(delta) else "red" if "-" in str(delta) else "gray"
        delta_html = f'<p class="metric-delta" style="color: {color};">{delta}</p>'
    
    card_html = f"""
    <div class="metric-card">
        <h3 class="metric-title">{title}</h3>
        <h2 class="metric-value">{value}</h2>
        {delta_html}
    </div>
    """
    
    return card_html

def generate_ubisoft_colors():
    """Palette de couleurs Ubisoft pour les graphiques"""
    return {
        'primary': '#0099CC',      # Bleu Ubisoft
        'secondary': '#FF6600',    # Orange
        'accent': '#00CC99',       # Turquoise
        'success': '#00AA44',      # Vert
        'warning': '#FFAA00',      # Orange foncé
        'danger': '#CC0044',       # Rouge
        'neutral': '#666666',      # Gris
        'light': '#F0F8FF',        # Bleu très clair
        'background': '#FFFFFF',   # Blanc
        'text': '#333333'          # Gris foncé
    }

def create_gaming_themed_chart(df, chart_type='bar', title="", **kwargs):
    """Crée des graphiques avec le thème gaming Ubisoft"""
    colors = generate_ubisoft_colors()
    
    # Configuration commune
    config = {
        'displayModeBar': False,
        'displaylogo': False
    }
    
    if chart_type == 'bar':
        fig = px.bar(df, **kwargs)
        fig.update_traces(marker_color=colors['primary'])
        
    elif chart_type == 'line':
        fig = px.line(df, **kwargs)
        fig.update_traces(line=dict(color=colors['primary'], width=3))
        
    elif chart_type == 'scatter':
        fig = px.scatter(df, **kwargs)
        fig.update_traces(marker=dict(color=colors['accent'], size=10))
        
    elif chart_type == 'pie':
        fig = px.pie(df, **kwargs)
        fig.update_traces(
            marker=dict(colors=[colors['primary'], colors['accent'], colors['success'], colors['warning']])
        )
    
    # Styling commun
    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            font=dict(size=18, family="Arial, sans-serif", color=colors['text'])
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial, sans-serif", color=colors['text']),
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig

def calculate_retention_roi(current_turnover, target_improvement, avg_salary, company_size):
    """Calcule le ROI d'amélioration de la rétention"""
    # Coût de remplacement = 1.5x le salaire annuel (standard RH)
    replacement_cost = avg_salary * 1.5
    
    # Nombre actuel de départs
    current_departures = company_size * (current_turnover / 100)
    
    # Coût annuel actuel
    current_annual_cost = current_departures * replacement_cost
    
    # Amélioration en nombre de départs évités
    departures_avoided = company_size * (target_improvement / 100)
    
    # Économies annuelles
    annual_savings = departures_avoided * replacement_cost
    
    return {
        'current_annual_cost': current_annual_cost,
        'annual_savings': annual_savings,
        'departures_avoided': departures_avoided,
        'roi_percentage': (annual_savings / current_annual_cost) * 100 if current_annual_cost > 0 else 0
    }

def create_neurodiversity_insights(df):
    """Génère des insights automatiques sur la neurodiversité"""
    insights = []
    
    # Corrélation neurodiversité/performance
    if 'Neurodiversity_Level' in df.columns and 'Innovation_Score' in df.columns:
        correlation = df['Neurodiversity_Level'].corr(df['Innovation_Score'])
        if correlation > 0.5:
            insights.append({
                'type': 'success',
                'title': '🧠 Strong Neurodiversity-Innovation Correlation',
                'message': f'Teams with higher neurodiversity show {correlation:.1%} correlation with innovation scores',
                'action': 'Consider expanding neurodiversity hiring initiatives'
            })
    
    # Tendances performance
    avg_performance = df.get('Team_Performance', pd.Series()).mean()
    if avg_performance > 85:
        insights.append({
            'type': 'info',
            'title': '🎯 High-Performing Teams',
            'message': f'Average team performance of {avg_performance:.1f}% indicates strong management practices',
            'action': 'Document and scale successful management approaches'
        })
    
    return insights

def export_data_to_csv(df, filename):
    """Exporte DataFrame vers CSV avec bouton download"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}" class="download-button">📥 Download {filename}</a>'
    return href

def display_gaming_easter_eggs():
    """Affiche des easter eggs gaming dans la sidebar"""
    gaming_quotes = [
        "🎮 'A delayed game is eventually good, but a rushed game is forever bad' - Shigeru Miyamoto",
        "🎯 'The best way to predict the future is to create it' - Gaming Industry Motto",
        "⚡ 'In gaming, diversity isn't just good practice - it's competitive advantage'",
        "🧠 'Neurodiversity in creative teams: Different minds, extraordinary games'",
        "🚀 'Data-driven decisions make legendary games'"
    ]
    
    if st.sidebar.button("🎮 Gaming Wisdom"):
        chosen_quote = np.random.choice(gaming_quotes)
        st.sidebar.info(chosen_quote)

def validate_data_quality(df, required_columns):
    """Valide la qualité des données"""
    issues = []
    
    # Vérifier les colonnes manquantes
    missing_cols = set(required_columns) - set(df.columns)
    if missing_cols:
        issues.append(f"❌ Missing columns: {', '.join(missing_cols)}")
    
    # Vérifier les valeurs manquantes
    for col in required_columns:
        if col in df.columns:
            missing_pct = (df[col].isnull().sum() / len(df)) * 100
            if missing_pct > 10:
                issues.append(f"⚠️ High missing values in {col}: {missing_pct:.1f}%")
    
    # Vérifier les doublons
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        issues.append(f"⚠️ Found {duplicates} duplicate rows")
    
    return issues

def create_animated_metric(value, target, label, unit=""):
    """Crée une métrique animée avec barre de progression"""
    progress = min(value / target, 1.0) if target > 0 else 0
    
    html = f"""
    <div class="animated-metric">
        <h4>{label}</h4>
        <div class="progress-container">
            <div class="progress-bar" style="width: {progress*100}%"></div>
        </div>
        <p class="metric-text">{value}{unit} / {target}{unit}</p>
    </div>
    """
    
    return html

def get_ubisoft_context():
    """Informations contextuelles Ubisoft pour personnalisation"""
    return {
        'founded': 1986,
        'headquarters': 'Saint-Mandé, France',
        'employees_global': '~20,000',
        'studios_worldwide': '40+',
        'major_franchises': [
            'Assassin\'s Creed', 'Rainbow Six', 'Far Cry', 
            'Just Dance', 'Watch Dogs', 'The Division'
        ],
        'diversity_commitment': 'Industry leader in D&I initiatives',
        'innovation_focus': 'AI, Cloud Gaming, Neurodiversity',
        'values': ['Dare', 'Create', 'Connect', 'Inspire']
    }
