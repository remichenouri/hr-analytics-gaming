"""Workforce Insights tab — headcount, turnover, and diversity KPIs."""

import streamlit as st
import pandas as pd
import plotly.express as px

from utils.helpers import PALETTE, apply_default_layout
from data.data_generator import FOCAL_COMPANY

# Discrete colour sequence aligned with the brand palette
_COMPANY_COLORS = [
    PALETTE["primary"], PALETTE["secondary"], PALETTE["accent"],
    PALETTE["warning"], PALETTE["neutral"],
]


def render_workforce_insights(df_workforce: pd.DataFrame) -> None:
    """Render the Workforce Insights tab.

    Args:
        df_workforce: Output of GamingIndustryDataGenerator.generate_workforce_data().
    """
    st.header("Workforce Insights")

    if df_workforce.empty:
        st.warning("No workforce data available.")
        return

    required = {"Company", "Turnover_Rate", "Employee_Satisfaction", "Diversity_Score", "Headcount"}
    missing = required - set(df_workforce.columns)
    if missing:
        st.error(f"Workforce data is missing columns: {', '.join(sorted(missing))}")
        return

    try:
        _render_kpi_row(df_workforce)
        _render_turnover_chart(df_workforce)
        _render_diversity_scatter(df_workforce)
        _render_headcount_trend(df_workforce)
        _render_insights(df_workforce)
    except Exception as exc:
        st.error(f"Error rendering Workforce Insights: {exc}")


# ── Private helpers ────────────────────────────────────────────────────────────

def _focal_vs_rest(df: pd.DataFrame, col: str) -> tuple[float, float]:
    """Return (focal mean, rest mean) for *col*, guarded against empty slices."""
    focal = df.loc[df["Company"] == FOCAL_COMPANY, col]
    rest = df.loc[df["Company"] != FOCAL_COMPANY, col]
    focal_mean = float(focal.mean()) if not focal.empty else 0.0
    rest_mean = float(rest.mean()) if not rest.empty else 0.0
    return focal_mean, rest_mean


def _render_kpi_row(df: pd.DataFrame) -> None:
    col1, col2, col3 = st.columns(3)

    turnover_focal, turnover_rest = _focal_vs_rest(df, "Turnover_Rate")
    sat_focal, sat_rest = _focal_vs_rest(df, "Employee_Satisfaction")
    div_focal, div_rest = _focal_vs_rest(df, "Diversity_Score")

    with col1:
        st.metric(
            f"{FOCAL_COMPANY} — Turnover Rate",
            f"{turnover_focal:.1f} %",
            f"{turnover_focal - turnover_rest:+.1f} pp vs industry avg",
            delta_color="inverse",  # lower is better
        )
    with col2:
        st.metric(
            "Employee Satisfaction",
            f"{sat_focal:.2f} / 5",
            f"{sat_focal - sat_rest:+.2f} vs industry avg",
        )
    with col3:
        st.metric(
            "Diversity Index",
            f"{div_focal:.2f}",
            f"{div_focal - div_rest:+.2f} vs industry avg",
        )


def _render_turnover_chart(df: pd.DataFrame) -> None:
    fig = px.box(
        df,
        x="Company",
        y="Turnover_Rate",
        color="Company",
        color_discrete_sequence=_COMPANY_COLORS,
        labels={"Turnover_Rate": "Annualised Turnover Rate (%)", "Company": "Studio"},
        points="all",
    )
    apply_default_layout(fig, "Turnover Rate Distribution — Gaming Studios")
    fig.update_layout(
        height=420,
        yaxis=dict(ticksuffix=" %", gridcolor="#e0e0e0"),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)


def _render_diversity_scatter(df: pd.DataFrame) -> None:
    fig = px.scatter(
        df,
        x="Diversity_Score",
        y="Employee_Satisfaction",
        size="Headcount",
        color="Company",
        color_discrete_sequence=_COMPANY_COLORS,
        hover_data={"Turnover_Rate": ":.1f", "Headcount": ":,"},
        labels={
            "Diversity_Score": "Diversity Index (0–1)",
            "Employee_Satisfaction": "Employee Satisfaction (1–5)",
            "Company": "Studio",
        },
        trendline="ols",
        size_max=40,
    )
    apply_default_layout(fig, "Diversity Index vs Employee Satisfaction")
    fig.update_layout(height=420)
    st.plotly_chart(fig, use_container_width=True)


def _render_headcount_trend(df: pd.DataFrame) -> None:
    if "Month" not in df.columns:
        return
    monthly = (
        df.groupby(["Month", "Company"], as_index=False)["Headcount"]
        .mean()
        .round(0)
    )
    fig = px.line(
        monthly,
        x="Month",
        y="Headcount",
        color="Company",
        color_discrete_sequence=_COMPANY_COLORS,
        markers=True,
        labels={"Month": "Month", "Headcount": "Average Headcount", "Company": "Studio"},
    )
    apply_default_layout(fig, "Monthly Headcount Trend")
    fig.update_layout(
        height=380,
        xaxis=dict(tickmode="linear", tick0=1, dtick=1, title="Month"),
        yaxis=dict(gridcolor="#e0e0e0"),
    )
    st.plotly_chart(fig, use_container_width=True)


def _render_insights(df: pd.DataFrame) -> None:
    st.subheader("Key Findings")

    turnover_focal, turnover_rest = _focal_vs_rest(df, "Turnover_Rate")
    sat_focal, sat_rest = _focal_vs_rest(df, "Employee_Satisfaction")
    div_focal, div_rest = _focal_vs_rest(df, "Diversity_Score")
    turnover_gap = turnover_focal - turnover_rest

    direction = "lower" if turnover_gap < 0 else "higher"
    st.info(
        f"**Turnover:** {FOCAL_COMPANY} runs {abs(turnover_gap):.1f} pp {direction} "
        f"than the industry average ({turnover_rest:.1f} %)."
    )
    st.info(
        f"**Satisfaction:** {FOCAL_COMPANY} scores {sat_focal:.2f}/5 "
        f"({'above' if sat_focal > sat_rest else 'below'} the industry mean of {sat_rest:.2f})."
    )
    st.info(
        f"**Diversity:** Index of {div_focal:.2f} vs industry average {div_rest:.2f} — "
        f"the OLS trendline above shows the positive correlation with satisfaction."
    )
    st.info(
        "**Opportunity:** Scaling inclusion programmes is projected to deliver a "
        "15–25 % innovation lift (see Neurodiversity tab)."
    )
