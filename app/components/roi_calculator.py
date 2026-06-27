"""ROI Calculator tab — cost-of-attrition and HR programme return analysis."""

import logging

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils.helpers import PALETTE, apply_default_layout

logger = logging.getLogger(__name__)

# ── Constants ──────────────────────────────────────────────────────────────────
REPLACEMENT_COST_MULTIPLIER = 1.8  # replacement = salary × 1.8 (fully-loaded cost)
FIVE_YEAR_DECAY = 0.90             # annual savings decay factor for multi-year projection
BUBBLE_SIZE_MAX = 40               # cap bubble marker size to avoid rendering issues
BUBBLE_SIZE_MIN = 5


def render_roi_calculator(df_roi: pd.DataFrame) -> None:
    """Render the ROI Calculator tab.

    Args:
        df_roi: Output of GamingIndustryDataGenerator.generate_roi_data().
    """
    st.header("ROI Calculator — Retention & Inclusion Programmes")

    if df_roi.empty:
        st.warning("No ROI data available.")
        return

    try:
        params = _render_input_section()
        results = _compute_roi(**params)
        _render_results_row(results)
        _render_scenario_charts(results, params)
        _render_five_year_projection(results)
        _render_recommendations(results)
    except Exception as exc:
        logger.exception("ROI Calculator rendering failed.")
        st.error(f"Calculation error: {exc}")


# ── Input section ──────────────────────────────────────────────────────────────

def _render_input_section() -> dict:
    """Render sliders/inputs and return a dict of parameter values."""
    st.subheader("Programme Parameters")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Company**")
        company_size = st.number_input("Headcount", 200, 10_000, 1_200, step=50)
        avg_salary = st.number_input("Avg annual salary (€)", 30_000, 200_000, 75_000, step=5_000)
        current_turnover = st.slider("Current turnover rate (%)", 5, 35, 15)

    with col2:
        st.markdown("**Investment**")
        programme_cost = st.number_input("Programme investment (€)", 10_000, 500_000, 150_000, step=10_000)
        cost_per_intervention = st.number_input("Cost per intervention (€)", 500, 20_000, 6_000, step=500)
        high_risk_n = st.number_input("High-risk employees (ML)", 5, 500, 75)
        medium_risk_n = st.number_input("Medium-risk employees (ML)", 5, 500, 120)

    with col3:
        st.markdown("**Effectiveness**")
        intervention_success = st.slider("Intervention success rate", 0.10, 0.90, 0.45, 0.05)
        targeting_precision = st.slider("ML targeting precision", 0.50, 0.99, 0.78, 0.01)
        model_accuracy = st.slider("Model accuracy", 0.55, 0.99, 0.82, 0.01)

    return dict(
        company_size=company_size,
        avg_salary=avg_salary,
        current_turnover=current_turnover,
        programme_cost=programme_cost,
        cost_per_intervention=cost_per_intervention,
        high_risk_n=high_risk_n,
        medium_risk_n=medium_risk_n,
        intervention_success=intervention_success,
        targeting_precision=targeting_precision,
        model_accuracy=model_accuracy,
    )


# ── ROI computation ────────────────────────────────────────────────────────────

def _compute_roi(
    company_size: int,
    avg_salary: float,
    current_turnover: float,
    programme_cost: float,
    cost_per_intervention: float,
    high_risk_n: int,
    medium_risk_n: int,
    intervention_success: float,
    targeting_precision: float,
    model_accuracy: float,
) -> dict:
    """Compute all ROI metrics from input parameters.

    Returns a flat dict of labelled results.
    """
    cost_per_departure = avg_salary * REPLACEMENT_COST_MULTIPLIER

    reachable_high = high_risk_n * 0.75 * targeting_precision
    reachable_med = medium_risk_n * 0.45 * targeting_precision
    total_reachable = reachable_high + reachable_med

    employees_saved = total_reachable * intervention_success
    total_savings = employees_saved * cost_per_departure

    total_intervention_cost = (high_risk_n + medium_risk_n) * cost_per_intervention
    total_cost = programme_cost + total_intervention_cost

    net_roi = total_savings - total_cost
    roi_pct = (net_roi / total_cost * 100.0) if total_cost > 0 else 0.0

    # Break-even in months (avoid division by zero)
    monthly_savings = total_savings / 12.0
    payback_months = (total_cost / monthly_savings) if monthly_savings > 0 else float("inf")

    confidence = model_accuracy * targeting_precision * intervention_success

    return dict(
        cost_per_departure=cost_per_departure,
        employees_saved=employees_saved,
        total_savings=total_savings,
        total_cost=total_cost,
        net_roi=net_roi,
        roi_pct=roi_pct,
        payback_months=payback_months,
        confidence=confidence,
        programme_cost=programme_cost,
        total_intervention_cost=total_intervention_cost,
        high_risk_n=high_risk_n,
        medium_risk_n=medium_risk_n,
        intervention_success=intervention_success,
        targeting_precision=targeting_precision,
    )


# ── Results row ────────────────────────────────────────────────────────────────

def _render_results_row(r: dict) -> None:
    st.subheader("Results")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Savings", f"€{r['total_savings']:,.0f}", f"{r['employees_saved']:.0f} departures avoided")
    c2.metric("Net ROI (Year 1)", f"€{r['net_roi']:,.0f}", f"{r['roi_pct']:+.0f} %")
    payback = f"{r['payback_months']:.1f} months" if r["payback_months"] != float("inf") else "N/A"
    c3.metric("Break-Even", payback)
    c4.metric("Confidence Score", f"{r['confidence']:.1%}", help="model accuracy × targeting precision × success rate")


# ── Charts ─────────────────────────────────────────────────────────────────────

def _render_scenario_charts(r: dict, params: dict) -> None:
    col1, col2 = st.columns(2)

    with col1:
        _render_bubble_chart(r, params)
    with col2:
        _render_waterfall_chart(r)


def _render_bubble_chart(r: dict, params: dict) -> None:
    """Scenario matrix: success rate × targeting precision → ROI %."""
    records = []
    for sr in np.arange(0.10, 0.91, 0.10):
        for pr in np.arange(0.50, 1.00, 0.05):
            reachable = (params["high_risk_n"] * 0.75 + params["medium_risk_n"] * 0.45) * pr
            savings = reachable * sr * r["cost_per_departure"]
            roi = (savings - r["total_cost"]) / r["total_cost"] * 100.0 if r["total_cost"] > 0 else 0.0
            records.append({"Success Rate": sr * 100, "Precision": pr * 100, "ROI %": roi})

    df_s = pd.DataFrame(records)

    # Clamp bubble sizes to avoid negative values from negative ROI
    raw_size = df_s["ROI %"]
    size_scaled = np.clip((raw_size - raw_size.min()) / max(raw_size.max() - raw_size.min(), 1e-9), 0, 1)
    bubble_sizes = (BUBBLE_SIZE_MIN + size_scaled * (BUBBLE_SIZE_MAX - BUBBLE_SIZE_MIN)).tolist()

    fig = go.Figure(go.Scatter(
        x=df_s["Success Rate"],
        y=df_s["Precision"],
        mode="markers",
        marker=dict(
            size=bubble_sizes,
            color=df_s["ROI %"],
            colorscale="RdYlGn",
            showscale=True,
            colorbar=dict(title="ROI %"),
        ),
        text=[f"ROI: {v:.0f}%<br>Conf: {s/100*p/100:.1%}"
              for v, s, p in zip(df_s["ROI %"], df_s["Success Rate"], df_s["Precision"])],
        hovertemplate="%{x:.0f}% success rate<br>%{y:.0f}% precision<br>%{text}<extra></extra>",
    ))
    apply_default_layout(fig, "ROI Sensitivity Matrix")
    fig.update_layout(
        height=440,
        xaxis=dict(title="Intervention Success Rate (%)", ticksuffix=" %"),
        yaxis=dict(title="ML Targeting Precision (%)", ticksuffix=" %"),
    )
    st.plotly_chart(fig, use_container_width=True)


def _render_waterfall_chart(r: dict) -> None:
    categories = ["Programme Cost", "Intervention Cost", "Savings", "Net ROI"]
    values = [-r["programme_cost"], -r["total_intervention_cost"], r["total_savings"], r["net_roi"]]

    fig = go.Figure(go.Waterfall(
        orientation="v",
        measure=["relative", "relative", "relative", "total"],
        x=categories,
        y=values,
        text=[f"€{abs(v):,.0f}" for v in values],
        textposition="outside",
        increasing=dict(marker=dict(color=PALETTE["success"])),
        decreasing=dict(marker=dict(color=PALETTE["danger"])),
        totals=dict(marker=dict(color=PALETTE["primary"])),
        connector=dict(line=dict(color=PALETTE["neutral"], width=1)),
    ))
    apply_default_layout(fig, "ROI Waterfall — Year 1")
    fig.update_layout(height=440, yaxis=dict(gridcolor="#e0e0e0"))
    st.plotly_chart(fig, use_container_width=True)


def _render_five_year_projection(r: dict) -> None:
    st.subheader("5-Year Cumulative ROI Projection")
    years = list(range(1, 6))
    cumulative: list[float] = []
    for k, _ in enumerate(years):
        yearly_savings = r["total_savings"] * (FIVE_YEAR_DECAY ** k)
        if k == 0:
            cumulative.append(yearly_savings - r["total_cost"])
        else:
            cumulative.append(cumulative[-1] + yearly_savings)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years, y=cumulative,
        mode="lines+markers",
        fill="tozeroy",
        fillcolor=f"rgba(23, 134, 122, 0.15)",
        line=dict(color=PALETTE["primary"], width=3),
        marker=dict(size=9),
        hovertemplate="Year %{x}<br>Cumulative ROI: €%{y:,.0f}<extra></extra>",
    ))
    fig.add_hline(y=0, line_dash="dash", line_color=PALETTE["danger"],
                  annotation_text="Break-even", annotation_position="bottom right")
    apply_default_layout(fig, "Cumulative ROI Over 5 Years")
    fig.update_layout(
        height=380,
        xaxis=dict(title="Year", tickvals=years),
        yaxis=dict(title="Cumulative ROI (€)", gridcolor="#e0e0e0"),
    )
    st.plotly_chart(fig, use_container_width=True)


def _render_recommendations(r: dict) -> None:
    st.subheader("Strategic Recommendations")
    roi = r["roi_pct"]

    if roi > 200:
        st.success("**Exceptional ROI** — Deploy the programme immediately and scale to all studios.")
        priority = "HIGH"
    elif roi > 100:
        st.info("**Strong ROI** — Sound investment with measurable returns. Begin pilot phase.")
        priority = "MEDIUM"
    elif roi > 0:
        st.warning("**Moderate ROI** — Optimise intervention targeting before full roll-out.")
        priority = "LOW"
    else:
        st.error("**Negative ROI** — Revisit cost structure or targeting strategy before proceeding.")
        priority = "REVIEW"

    recs = [
        f"**ML Targeting:** {r['high_risk_n']} high-risk employees identified as priority for intervention.",
        f"**Budget:** €{r['total_cost']:,.0f} total investment to prevent ~{r['employees_saved']:.0f} departures.",
        "**Monitoring:** Track monthly retention rate to validate programme effectiveness.",
        "**Model refresh:** Retrain the churn model every 6 months on updated data.",
    ]
    for i, rec in enumerate(recs, 1):
        st.markdown(f"{i}. {rec}")

    if priority in ("HIGH", "MEDIUM"):
        st.markdown("**Suggested next steps:**")
        steps = [
            "Secure budget sign-off from HR leadership.",
            "Launch a 3-month pilot on the highest-risk cohort.",
            "Set up a real-time retention monitoring dashboard.",
            "Train HR Business Partners on model output interpretation.",
        ]
        for step in steps:
            st.markdown(f"- {step}")
