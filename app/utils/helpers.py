"""Shared utilities: colour palette, number formatting, chart helpers, data validation."""

import base64
import logging

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

logger = logging.getLogger(__name__)

# ── Brand palette ──────────────────────────────────────────────────────────────
PALETTE: dict[str, str] = {
    "primary":    "#17867A",  # teal
    "secondary":  "#F4845F",  # warm orange
    "accent":     "#2EC4B6",  # light teal
    "success":    "#22A06B",  # green
    "warning":    "#F5A623",  # amber
    "danger":     "#D63031",  # red
    "neutral":    "#636E72",  # grey
    "light":      "#E8F5F3",  # pale teal
    "background": "#FFFFFF",
    "text":       "#2D3436",
}

CHART_LAYOUT_DEFAULTS: dict = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Arial, sans-serif", color=PALETTE["text"], size=13),
    margin=dict(l=40, r=20, t=60, b=40),
    title=dict(x=0.5, xanchor="center", font=dict(size=17, color=PALETTE["text"])),
    legend=dict(bgcolor="rgba(0,0,0,0)", borderwidth=0),
)


# ── Formatting ─────────────────────────────────────────────────────────────────

def format_number(value: float, prefix: str = "", suffix: str = "") -> str:
    """Return a human-readable string for *value* with optional prefix/suffix.

    Handles NaN, billions, millions, thousands, and plain integers/floats.
    """
    if pd.isna(value):
        return "N/A"
    try:
        value = float(value)
    except (TypeError, ValueError):
        return str(value)

    abs_val = abs(value)
    if abs_val >= 1e9:
        formatted = f"{value / 1e9:.1f}B"
    elif abs_val >= 1e6:
        formatted = f"{value / 1e6:.1f}M"
    elif abs_val >= 1e3:
        formatted = f"{value / 1e3:.1f}K"
    elif value == int(value):
        formatted = f"{int(value):,}"
    else:
        formatted = f"{value:,.1f}"

    return f"{prefix}{formatted}{suffix}"


# ── CSS loader ─────────────────────────────────────────────────────────────────

def load_css(file_path: str) -> bool:
    """Inject a CSS file into the Streamlit page.

    Returns True on success, False on failure (non-fatal).
    """
    try:
        with open(file_path) as fh:
            st.markdown(f"<style>{fh.read()}</style>", unsafe_allow_html=True)
        return True
    except FileNotFoundError:
        logger.warning("CSS file not found: %s", file_path)
        return False
    except OSError as exc:
        logger.error("Error loading CSS %s: %s", file_path, exc)
        return False


# ── Chart helpers ──────────────────────────────────────────────────────────────

def apply_default_layout(fig: go.Figure, title: str = "") -> go.Figure:
    """Apply the shared brand layout to any Plotly figure in-place."""
    updates = dict(**CHART_LAYOUT_DEFAULTS)
    if title:
        updates["title"] = dict(**CHART_LAYOUT_DEFAULTS["title"], text=title)
    fig.update_layout(**updates)
    return fig


def create_bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    color: str | None = None,
    orientation: str = "v",
    **kwargs,
) -> go.Figure:
    """Return a branded Plotly bar chart."""
    fig = px.bar(df, x=x, y=y, color=color, orientation=orientation, **kwargs)
    fig.update_traces(marker_color=PALETTE["primary"] if color is None else None)
    apply_default_layout(fig, title)
    return fig


def create_line_chart(
    df: pd.DataFrame,
    x: str,
    y: str | list[str],
    title: str = "",
    **kwargs,
) -> go.Figure:
    """Return a branded Plotly line chart."""
    fig = px.line(df, x=x, y=y, **kwargs)
    fig.update_traces(line=dict(width=2.5))
    apply_default_layout(fig, title)
    return fig


def create_scatter_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    **kwargs,
) -> go.Figure:
    """Return a branded Plotly scatter chart."""
    fig = px.scatter(df, x=x, y=y, **kwargs)
    apply_default_layout(fig, title)
    return fig


# ── KPI calculations ───────────────────────────────────────────────────────────

def calculate_retention_roi(
    current_turnover_pct: float,
    improvement_pct: float,
    avg_salary: float,
    company_size: int,
) -> dict[str, float]:
    """Return cost-of-attrition metrics for a given retention improvement scenario.

    Uses the standard HR convention: replacement cost = 1.5 × annual salary.

    Args:
        current_turnover_pct: Annualised turnover rate (0–100).
        improvement_pct: Target reduction in turnover rate (percentage points).
        avg_salary: Average annual salary in the local currency.
        company_size: Total headcount.

    Returns:
        Dictionary with keys: current_annual_cost, annual_savings,
        departures_avoided, roi_percentage.
    """
    if company_size <= 0:
        raise ValueError("company_size must be positive.")
    if avg_salary <= 0:
        raise ValueError("avg_salary must be positive.")

    replacement_cost = avg_salary * 1.5
    current_departures = company_size * (current_turnover_pct / 100.0)
    current_annual_cost = current_departures * replacement_cost
    departures_avoided = company_size * (improvement_pct / 100.0)
    annual_savings = departures_avoided * replacement_cost
    roi_pct = (annual_savings / current_annual_cost * 100.0) if current_annual_cost > 0 else 0.0

    return {
        "current_annual_cost": current_annual_cost,
        "annual_savings": annual_savings,
        "departures_avoided": departures_avoided,
        "roi_percentage": roi_pct,
    }


# ── Data validation ────────────────────────────────────────────────────────────

def validate_dataframe(df: pd.DataFrame, required_columns: list[str]) -> list[str]:
    """Return a list of data-quality issues found in *df*.

    Checks: missing columns, high null rates (> 10 %), duplicate rows.
    """
    issues: list[str] = []

    missing = set(required_columns) - set(df.columns)
    if missing:
        issues.append(f"Missing columns: {', '.join(sorted(missing))}")

    for col in required_columns:
        if col not in df.columns:
            continue
        null_pct = df[col].isna().mean() * 100
        if null_pct > 10:
            issues.append(f"High null rate in '{col}': {null_pct:.1f} %")

    dupes = int(df.duplicated().sum())
    if dupes:
        issues.append(f"{dupes} duplicate rows detected.")

    return issues


# ── Metric card ────────────────────────────────────────────────────────────────

def metric_card_html(title: str, value: str, delta: str | None = None) -> str:
    """Return an HTML snippet for a styled metric card."""
    delta_html = f'<p style="margin:0;color:{PALETTE["neutral"]};font-size:0.85rem;">{delta}</p>' if delta else ""
    return (
        f'<div class="metric-card">'
        f'<p style="margin:0;font-size:0.85rem;color:{PALETTE["neutral"]};">{title}</p>'
        f'<h2 style="margin:0.2rem 0;color:{PALETTE["primary"]};">{value}</h2>'
        f"{delta_html}"
        f"</div>"
    )


# ── CSV export ─────────────────────────────────────────────────────────────────

def dataframe_download_link(df: pd.DataFrame, filename: str) -> str:
    """Return an HTML anchor tag that downloads *df* as a CSV file."""
    csv_bytes = df.to_csv(index=False).encode()
    b64 = base64.b64encode(csv_bytes).decode()
    return (
        f'<a href="data:file/csv;base64,{b64}" download="{filename}" '
        f'style="color:{PALETTE["primary"]};font-weight:600;">&#8595; Download {filename}</a>'
    )


# ── Sidebar extras ─────────────────────────────────────────────────────────────

def display_sidebar_quote() -> None:
    """Show a rotating gaming wisdom quote in the sidebar."""
    quotes = [
        "'A delayed game is eventually good, but a rushed game is forever bad.' — Shigeru Miyamoto",
        "'In gaming, diversity is not just good practice — it is competitive advantage.'",
        "'Different minds build extraordinary games.'",
        "'Data-driven decisions make legendary products.'",
    ]
    if st.sidebar.button("Gaming Wisdom"):
        rng = np.random.default_rng()
        st.sidebar.info(quotes[int(rng.integers(len(quotes)))])
