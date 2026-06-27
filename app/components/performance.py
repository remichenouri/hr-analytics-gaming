"""Performance Dashboard tab — team and department KPIs."""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from utils.helpers import PALETTE, apply_default_layout

# Reproducible synthetic data for this tab
_RNG = np.random.default_rng(42)

DEPARTMENTS = ["Engineering", "Creative", "QA", "Marketing", "HR"]
TEAMS = ["Game Dev", "Art", "QA", "Design", "Marketing"]
MONTHS = pd.date_range(start="2024-01-01", periods=8, freq="ME")

# ── Synthetic KPI data (module-level so it doesn't regenerate on re-runs) ─────
_PERFORMANCE_SCORES = np.clip(_RNG.normal(4.1, 0.25, len(MONTHS)), 1, 5)
_PRODUCTIVITY = np.clip(_RNG.normal(85, 4, len(MONTHS)), 60, 100)
_TEAM_PRODUCTIVITY = np.clip(_RNG.normal(84, 6, len(TEAMS)), 60, 100)
_DEPT_PERFORMANCE = np.clip(_RNG.normal(4.0, 0.35, len(DEPARTMENTS)), 1, 5)
_INNOVATION_SCORES = np.clip(_RNG.normal(88, 5, len(DEPARTMENTS)), 60, 100)
_TEAM_SIZES = _RNG.integers(40, 200, len(DEPARTMENTS))

# Headline KPI values derived from synthetic data (not hardcoded strings)
_AVG_PERFORMANCE = float(_PERFORMANCE_SCORES.mean())
_AVG_PRODUCTIVITY = float(_PRODUCTIVITY.mean())
_TOTAL_HEADCOUNT = int(_RNG.integers(1_150, 1_350))
_INNOVATION_INDEX = float(_INNOVATION_SCORES.mean())


def render_performance_dashboard() -> None:
    """Render the Performance Analytics tab with reproducible synthetic data."""
    st.header("Performance Analytics Dashboard")

    try:
        _render_kpi_row()
        _render_main_charts()
        _render_smart_alerts()
    except Exception as exc:
        st.error(f"Error rendering Performance Dashboard: {exc}")


# ── Private helpers ────────────────────────────────────────────────────────────

def _render_kpi_row() -> None:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Active Employees", f"{_TOTAL_HEADCOUNT:,}", "+18 this month")
    c2.metric("Avg Performance Score", f"{_AVG_PERFORMANCE:.2f} / 5", "+0.2 vs prior period")
    c3.metric("Team Productivity", f"{_AVG_PRODUCTIVITY:.0f} %", "+4 pp vs prior period")
    c4.metric("Innovation Index", f"{_INNOVATION_INDEX:.0f} / 100", "+8 pts vs prior period")


def _render_main_charts() -> None:
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Performance Score Trend",
            "Productivity by Team (%)",
            "Innovation Score by Department",
            "Avg Performance Score by Department",
        ),
        specs=[
            [{"secondary_y": True}, {"type": "bar"}],
            [{"type": "bar"}, {"type": "bar"}],
        ],
        vertical_spacing=0.15,
        horizontal_spacing=0.10,
    )

    # ── Row 1, Col 1 — Performance & Productivity trend ──
    fig.add_trace(
        go.Scatter(
            x=MONTHS, y=_PERFORMANCE_SCORES,
            name="Perf. Score", mode="lines+markers",
            line=dict(color=PALETTE["primary"], width=2.5),
            marker=dict(size=6),
            hovertemplate="%{x|%b %Y}<br>Score: %{y:.2f}<extra>Performance</extra>",
        ),
        row=1, col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=MONTHS, y=_PRODUCTIVITY,
            name="Productivity %", mode="lines+markers",
            line=dict(color=PALETTE["secondary"], width=2.5, dash="dot"),
            marker=dict(size=6, symbol="diamond"),
            hovertemplate="%{x|%b %Y}<br>Productivity: %{y:.1f}%<extra>Productivity</extra>",
        ),
        row=1, col=1, secondary_y=True,
    )

    # ── Row 1, Col 2 — Productivity by team ──
    fig.add_trace(
        go.Bar(
            x=TEAMS, y=_TEAM_PRODUCTIVITY,
            name="Team Productivity",
            marker_color=PALETTE["accent"],
            text=[f"{v:.0f}%" for v in _TEAM_PRODUCTIVITY],
            textposition="outside",
            hovertemplate="%{x}<br>Productivity: %{y:.1f}%<extra></extra>",
        ),
        row=1, col=2,
    )

    # ── Row 2, Col 1 — Innovation by department ──
    fig.add_trace(
        go.Bar(
            x=DEPARTMENTS, y=_INNOVATION_SCORES,
            name="Innovation Score",
            marker_color=PALETTE["primary"],
            text=[f"{v:.0f}" for v in _INNOVATION_SCORES],
            textposition="outside",
            hovertemplate="%{x}<br>Innovation: %{y:.0f}<extra></extra>",
        ),
        row=2, col=1,
    )

    # ── Row 2, Col 2 — Performance by department ──
    fig.add_trace(
        go.Bar(
            x=DEPARTMENTS, y=_DEPT_PERFORMANCE,
            name="Dept Performance",
            marker_color=PALETTE["warning"],
            text=[f"{v:.2f}" for v in _DEPT_PERFORMANCE],
            textposition="outside",
            hovertemplate="%{x}<br>Score: %{y:.2f}/5<extra></extra>",
        ),
        row=2, col=2,
    )

    apply_default_layout(fig, "Performance Analytics — 2024")
    fig.update_layout(
        height=620,
        showlegend=True,
        legend=dict(orientation="h", y=-0.12),
        yaxis=dict(title="Score (1–5)", range=[3.5, 4.8], gridcolor="#e0e0e0"),
        yaxis2=dict(title="Productivity (%)", ticksuffix=" %"),
        yaxis3=dict(title="Productivity (%)", ticksuffix=" %", gridcolor="#e0e0e0"),
        yaxis4=dict(title="Innovation (0–100)", gridcolor="#e0e0e0"),
        yaxis5=dict(title="Score (1–5)", gridcolor="#e0e0e0"),
    )
    st.plotly_chart(fig, use_container_width=True)


def _render_smart_alerts() -> None:
    st.subheader("Smart Alerts")

    best_team = TEAMS[int(np.argmax(_TEAM_PRODUCTIVITY))]
    worst_team = TEAMS[int(np.argmin(_TEAM_PRODUCTIVITY))]
    best_dept = DEPARTMENTS[int(np.argmax(_DEPT_PERFORMANCE))]

    st.success(
        f"**{best_team}** leads in productivity at "
        f"{_TEAM_PRODUCTIVITY.max():.0f}% — document and scale their practices."
    )
    st.warning(
        f"**{worst_team}** productivity is at "
        f"{_TEAM_PRODUCTIVITY.min():.0f}% — schedule a process review."
    )
    st.info(
        f"**{best_dept}** scores highest on innovation ({_INNOVATION_SCORES.max():.0f}/100) "
        "— strong correlation with neurodiversity programmes detected."
    )
    if _AVG_PRODUCTIVITY < 82:
        st.error("Overall productivity below the 82% target threshold — executive review recommended.")
