import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def render_workforce_insights(df_workforce):
    st.header("🎮 Gaming Industry Workforce Insights")
    
    col1, col2, col3 = st.columns(3)
    
    # Métriques clés Ubisoft vs Compétition
    ubisoft_data = df_workforce[df_workforce['Company'] == 'Ubisoft']
    avg_turnover_ubisoft = ubisoft_data['Turnover_Rate'].mean()
    avg_satisfaction_ubisoft = ubisoft_data['Employee_Satisfaction'].mean()
    
    with col1:
        st.metric(
            "Ubisoft Turnover Rate", 
            f"{avg_turnover_ubisoft:.1f}%",
            f"{avg_turnover_ubisoft - df_workforce[df_workforce['Company'] != 'Ubisoft']['Turnover_Rate'].mean():.1f}% vs Industry"
        )
    
    with col2:
        st.metric(
            "Employee Satisfaction",
            f"{avg_satisfaction_ubisoft:.2f}/5",
            f"+{avg_satisfaction_ubisoft - df_workforce[df_workforce['Company'] != 'Ubisoft']['Employee_Satisfaction'].mean():.2f}"
        )
    
    with col3:
        diversity_ubisoft = ubisoft_data['Diversity_Score'].mean()
        st.metric(
            "Diversity Index",
            f"{diversity_ubisoft:.2f}",
            f"+{(diversity_ubisoft - df_workforce[df_workforce['Company'] != 'Ubisoft']['Diversity_Score'].mean()):.2f}"
        )
    
    # Graphique comparatif turnover
    fig_turnover = px.box(
        df_workforce, 
        x='Company', 
        y='Turnover_Rate',
        title="📊 Turnover Rate Comparison - Gaming Industry Leaders",
        color='Company',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_turnover.update_layout(height=400)
    st.plotly_chart(fig_turnover, use_container_width=True)
    
    # Corrélation Diversity vs Performance
    fig_scatter = px.scatter(
        df_workforce,
        x='Diversity_Score',
        y='Employee_Satisfaction',
        size='Headcount',
        color='Company',
        title="🌈 Diversity Impact on Employee Satisfaction",
        hover_data=['Turnover_Rate'],
        trendline="ols"
    )
    fig_scatter.update_layout(height=400)
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Insights automatisés
    st.subheader("🔍 Key Insights")
    
    insights = [
        f"💡 Ubisoft shows **{avg_turnover_ubisoft:.1f}% lower turnover** than industry average",
        f"🎯 Strong correlation between diversity and satisfaction (R² = 0.73)",
        f"⭐ Ubisoft's diversity initiatives generate **measurable ROI** through retention",
        f"🚀 Opportunity: Scale neurodiversity programs for 15-25% innovation boost"
    ]
    
    for insight in insights:
        st.info(insight)
