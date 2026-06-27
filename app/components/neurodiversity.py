"""Neurodiversity Impact tab — inclusion metrics and innovation correlation analysis."""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.helpers import PALETTE, apply_default_layout


def render_neurodiversity_analysis(df_neuro: pd.DataFrame) -> None:
    """Render the Neurodiversity Impact tab.

    Args:
        df_neuro: Output of GamingIndustryDataGenerator.generate_neurodiversity_data().
    """
    st.header("Neurodiversity in Creative Teams — Impact Analysis")

    if df_neuro.empty:
        st.warning("No neurodiversity data available.")
        return

    required = {
        "Neurodiversity_Percentage", "Innovation_Score",
        "Creativity_Index", "Problem_Solving_Score", "Team_Performance",
    }
    missing = required - set(df_neuro.columns)
    if missing:
        st.error(f"Data is missing columns: {', '.join(sorted(missing))}")
        return

    try:
        _render_kpi_row(df_neuro)
        _render_innovation_scatter(df_neuro)
        _render_dual_axis_trend(df_neuro)
        _render_recommendations(df_neuro)
    except Exception as exc:
        st.error(f"Error rendering Neurodiversity tab: {exc}")


# ── Private helpers ────────────────────────────────────────────────────────────

def _optimal_row(df: pd.DataFrame) -> pd.Series:
    """Return the row with the highest Innovation_Score."""
    idx = df["Innovation_Score"].idxmax()
    return df.loc[idx]


def _render_kpi_row(df: pd.DataFrame) -> None:
    col1, col2, col3, col4 = st.columns(4)
    best = _optimal_row(df)

    perf_range = float(df["Team_Performance"].max()) - float(df["Team_Performance"].min())
    innov_range = float(df["Innovation_Score"].max()) - float(df["Innovation_Score"].min())

    with col1:
        st.metric(
            "Optimal Neurodiversity %",
            f"{best['Neurodiversity_Percentage']:.1f} %",
            "for peak innovation",
        )
    with col2:
        st.metric(
            "Max Innovation Gain",
            f"+{innov_range:.0f} pts",
            "low → high neurodiversity",
        )
    with col3:
        st.metric(
            "Creativity Index (peak)",
            f"{best['Creativity_Index']:.2f}",
        )
    with col4:
        st.metric(
            "Team Performance Gain",
            f"+{perf_range:.1f} pts",
            "across the full spectrum",
        )


def _render_innovation_scatter(df: pd.DataFrame) -> None:
    fig = px.scatter(
        df,
        x="Neurodiversity_Percentage",
        y="Innovation_Score",
        size="Team_Performance",
        color="Creativity_Index",
        color_continuous_scale=[
            [0.0, PALETTE["light"]],
            [0.5, PALETTE["accent"]],
            [1.0, PALETTE["primary"]],
        ],
        labels={
            "Neurodiversity_Percentage": "Neurodiversity Level (%)",
            "Innovation_Score": "Innovation Score (0–100)",
            "Team_Performance": "Team Performance",
            "Creativity_Index": "Creativity Index",
        },
        hover_data={
            "Problem_Solving_Score": ":.1f",
            "Team_Performance": ":.1f",
        },
        trendline="lowess",
        size_max=30,
    )
    apply_default_layout(fig, "Innovation Score vs Neurodiversity Level")
    fig.update_layout(height=480, coloraxis_colorbar=dict(title="Creativity"))
    st.plotly_chart(fig, use_container_width=True)


def _render_dual_axis_trend(df: pd.DataFrame) -> None:
    x = df["Neurodiversity_Percentage"]
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x,
        y=df["Innovation_Score"],
        mode="lines+markers",
        name="Innovation Score",
        line=dict(color=PALETTE["primary"], width=2.5),
        marker=dict(size=6),
        hovertemplate="Neurodiversity: %{x:.1f}%<br>Innovation: %{y:.1f}<extra></extra>",
    ))

    fig.add_trace(go.Scatter(
        x=x,
        y=df["Problem_Solving_Score"],
        mode="lines+markers",
        name="Problem Solving",
        line=dict(color=PALETTE["secondary"], width=2.5, dash="dash"),
        marker=dict(size=6, symbol="diamond"),
        yaxis="y2",
        hovertemplate="Neurodiversity: %{x:.1f}%<br>Problem Solving: %{y:.1f}<extra></extra>",
    ))

    apply_default_layout(fig, "Neurodiversity Impact on Key Metrics")
    fig.update_layout(
        height=420,
        xaxis=dict(title="Neurodiversity Level (%)", ticksuffix=" %"),
        yaxis=dict(title="Innovation Score", titlefont=dict(color=PALETTE["primary"]),
                   tickfont=dict(color=PALETTE["primary"]), gridcolor="#e0e0e0"),
        yaxis2=dict(title="Problem Solving Score", titlefont=dict(color=PALETTE["secondary"]),
                    tickfont=dict(color=PALETTE["secondary"]), overlaying="y", side="right"),
        legend=dict(x=0.01, y=0.99),
    )
    st.plotly_chart(fig, use_container_width=True)


def _render_recommendations(df: pd.DataFrame) -> None:
    st.subheader("Data-Driven Recommendations")
    best = _optimal_row(df)

    recs = [
        {
            "title": "Target Neurodiversity Level",
            "body": (
                f"Aim for **{best['Neurodiversity_Percentage']:.1f} %** neurodiverse team "
                "composition to maximise innovation output."
            ),
            "impact": "High",
        },
        {
            "title": "Neurodiversity-Aware Creative Workflows",
            "body": (
                "Implement structured ideation sessions and flexible communication "
                "norms to leverage diverse cognitive styles in game development."
            ),
            "impact": "Medium",
        },
        {
            "title": "Monthly KPI Tracking",
            "body": (
                "Monitor creativity and innovation scores monthly. "
                "The data shows a positive, non-linear relationship — early gains "
                "accelerate as inclusion practices mature."
            ),
            "impact": "High",
        },
    ]

    for rec in recs:
        label = f"**{rec['title']}** — Impact: {rec['impact']}"
        with st.expander(label):
            st.markdown(rec["body"])
