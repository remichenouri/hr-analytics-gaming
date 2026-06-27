import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def render_neurodiversity_analysis(df_neuro):
    st.header("🧠 Neurodiversity in Creative Teams - Impact Analysis")
    
    # Statistiques clés
    col1, col2, col3, col4 = st.columns(4)
    
    optimal_diversity = df_neuro.loc[df_neuro['Innovation_Score'].idxmax()]
    
    with col1:
        st.metric(
            "Optimal Neurodiversity %", 
            f"{optimal_diversity['Neurodiversity_Percentage']:.1f}%",
            "For Max Innovation"
        )
    
    with col2:
        st.metric(
            "Innovation Boost",
            f"+{optimal_diversity['Innovation_Score'] - df_neuro['Innovation_Score'].min():.0f}%",
            "vs Baseline"
        )
    
    with col3:
        st.metric(
            "Creativity Index Peak",
            f"{optimal_diversity['Creativity_Index']:.2f}",
            "Industry Leading"
        )
    
    with col4:
        avg_performance_gain = (df_neuro['Team_Performance'].max() - df_neuro['Team_Performance'].min())
        st.metric(
            "Team Performance Gain",
            f"+{avg_performance_gain:.1f}%",
            "With Inclusion"
        )
    
    # Graphique principal : Innovation vs Neurodiversity
    fig_innovation = px.scatter(
        df_neuro,
        x='Neurodiversity_Percentage',
        y='Innovation_Score',
        size='Team_Performance',
        color='Creativity_Index',
        title="🚀 Innovation Score vs Neurodiversity Level",
        labels={'Neurodiversity_Percentage': 'Neurodiversity %', 'Innovation_Score': 'Innovation Score'},
        color_continuous_scale='viridis',
        trendline="lowess"
    )
    fig_innovation.update_layout(height=500)
    st.plotly_chart(fig_innovation, use_container_width=True)
    
    # Multi-métriques dashboard
    fig_multi = go.Figure()
    
    fig_multi.add_trace(go.Scatter(
        x=df_neuro['Neurodiversity_Percentage'],
        y=df_neuro['Innovation_Score'],
        mode='lines+markers',
        name='Innovation Score',
        line=dict(color='blue', width=3)
    ))
    
    fig_multi.add_trace(go.Scatter(
        x=df_neuro['Neurodiversity_Percentage'],
        y=df_neuro['Problem_Solving_Score'],
        mode='lines+markers',
        name='Problem Solving',
        line=dict(color='red', width=3),
        yaxis='y2'
    ))
    
    fig_multi.update_layout(
        title="📈 Neurodiversity Impact on Key Performance Metrics",
        xaxis_title="Neurodiversity Percentage",
        yaxis=dict(title="Innovation Score", side="left", color="blue"),
        yaxis2=dict(title="Problem Solving Score", side="right", overlaying="y", color="red"),
        height=400
    )
    
    st.plotly_chart(fig_multi, use_container_width=True)
    
    # Recommandations basées sur data
    st.subheader("🎯 Data-Driven Recommendations for Ubisoft")
    
    recommendations = [
        {
            "title": "🎯 Target Neurodiversity Level",
            "content": f"Achieve **{optimal_diversity['Neurodiversity_Percentage']:.1f}%** neurodivergent team composition for maximum innovation output",
            "impact": "High"
        },
        {
            "title": "🛠️ Creative Process Optimization", 
            "content": "Implement neurodiversity-aware creative workflows in game development teams",
            "impact": "Medium"
        },
        {
            "title": "📊 Continuous Monitoring",
            "content": "Track creativity and innovation metrics monthly to optimize team composition",
            "impact": "High"
        }
    ]
    
    for rec in recommendations:
        with st.expander(f"{rec['title']} - Impact: {rec['impact']}"):
            st.write(rec['content'])
