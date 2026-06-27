"""Retention Models tab — ML churn prediction with a temporal validation split."""

import logging
import os

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import TimeSeriesSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from utils.helpers import PALETTE, apply_default_layout

logger = logging.getLogger(__name__)

# ── Constants ──────────────────────────────────────────────────────────────────
SAFE_FEATURES = [
    "tenure_months",
    "salary_vs_market",
    "days_since_promotion",
    "manager_tenure_months",
    "team_size",
    "is_neurodivergent",
    "department_encoded",
    "level_encoded",
]
NUMERIC_FEATURES = [
    "tenure_months", "salary_vs_market", "days_since_promotion",
    "manager_tenure_months", "team_size",
]
PASSTHROUGH_FEATURES = ["is_neurodivergent", "department_encoded", "level_encoded"]

DEPT_ENCODING = {"Engineering": 1, "Art": 2, "Design": 3, "QA": 4, "Production": 5}
LEVEL_ENCODING = {"Junior": 1, "Senior": 2, "Lead": 3, "Principal": 4}

TRAIN_RATIO = 0.80
N_CV_SPLITS = 3
MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")


# ── Public entry-point ─────────────────────────────────────────────────────────

def render_retention_models(df_retention: pd.DataFrame) -> None:
    """Render the Talent Retention tab.

    Args:
        df_retention: Output of GamingIndustryDataGenerator.generate_retention_data().
    """
    st.header("Talent Retention — Predictive Model")

    if df_retention.empty:
        st.warning("No retention data available.")
        return

    try:
        with st.spinner("Preparing features and training model…"):
            df_clean = _prepare_features(df_retention.copy())
            model, metrics, feature_importance = _train_model(df_clean)

        _render_metrics_row(metrics)
        _render_feature_importance(feature_importance)
        _render_risk_calculator(model)
        _render_model_save(model)

    except Exception as exc:
        logger.exception("Retention model rendering failed.")
        st.error(f"Model error: {exc}")


# ── Feature engineering ────────────────────────────────────────────────────────

def _prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add synthetic temporal features and a binary attrition target to *df*."""
    rng = np.random.default_rng(42)

    df["snapshot_date"] = pd.date_range(
        start="2022-01-01", periods=len(df), freq="D"
    )
    df["tenure_months"] = rng.integers(1, 121, len(df))
    df["salary_vs_market"] = rng.uniform(0.80, 1.40, len(df)).round(3)
    df["days_since_promotion"] = rng.integers(0, 1096, len(df))
    df["manager_tenure_months"] = rng.integers(6, 85, len(df))
    df["team_size"] = rng.integers(3, 21, len(df))
    df["department_encoded"] = rng.integers(1, 6, len(df))
    df["level_encoded"] = rng.integers(1, 5, len(df))
    df["will_leave_6m"] = rng.binomial(1, 0.15, len(df))

    if "Is_Neurodivergent" in df.columns:
        df["is_neurodivergent"] = df["Is_Neurodivergent"].astype(int)
    else:
        df["is_neurodivergent"] = rng.binomial(1, 0.12, len(df))

    return df


# ── Model training ─────────────────────────────────────────────────────────────

@st.cache_resource(show_spinner=False)
def _train_model(df: pd.DataFrame) -> tuple[Pipeline, dict, pd.DataFrame]:
    """Train a Gradient Boosting classifier with temporal validation.

    Cached with st.cache_resource so re-runs do not retrain.
    """
    cutoff = df["snapshot_date"].quantile(TRAIN_RATIO)
    train_mask = df["snapshot_date"] <= cutoff

    X_train = df.loc[train_mask, SAFE_FEATURES]
    X_test = df.loc[~train_mask, SAFE_FEATURES]
    y_train = df.loc[train_mask, "will_leave_6m"]
    y_test = df.loc[~train_mask, "will_leave_6m"]

    preprocessor = ColumnTransformer([
        ("num", StandardScaler(), NUMERIC_FEATURES),
        ("cat", "passthrough", PASSTHROUGH_FEATURES),
    ])
    model = Pipeline([
        ("prep", preprocessor),
        ("clf", GradientBoostingClassifier(
            n_estimators=100, max_depth=4, learning_rate=0.1, random_state=42,
        )),
    ])
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    accuracy = float(accuracy_score(y_test, y_pred))
    auc = float(roc_auc_score(y_test, y_proba)) if len(np.unique(y_test)) > 1 else float("nan")

    tscv = TimeSeriesSplit(n_splits=N_CV_SPLITS)
    cv_aucs: list[float] = []
    for tr_idx, val_idx in tscv.split(X_train):
        model.fit(X_train.iloc[tr_idx], y_train.iloc[tr_idx])
        val_proba = model.predict_proba(X_train.iloc[val_idx])[:, 1]
        y_val = y_train.iloc[val_idx]
        if len(np.unique(y_val)) > 1:
            cv_aucs.append(roc_auc_score(y_val, val_proba))

    # Re-fit on full training set after CV loop
    model.fit(X_train, y_train)

    feature_importance = pd.DataFrame({
        "Feature": SAFE_FEATURES,
        "Importance": model.named_steps["clf"].feature_importances_,
    }).sort_values("Importance", ascending=True)

    metrics = {
        "accuracy": accuracy,
        "auc": auc,
        "cv_mean": float(np.mean(cv_aucs)) if cv_aucs else float("nan"),
        "cv_std": float(np.std(cv_aucs)) if cv_aucs else float("nan"),
        "train_n": int(train_mask.sum()),
        "test_n": int((~train_mask).sum()),
        "retention_rate": float(1 - y_train.mean()),
    }
    return model, metrics, feature_importance


# ── Rendering helpers ──────────────────────────────────────────────────────────

def _render_metrics_row(metrics: dict) -> None:
    st.info(
        f"**Training set:** {metrics['train_n']:,} employees · "
        f"**Hold-out (temporal):** {metrics['test_n']:,} employees"
    )
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Test Accuracy", f"{metrics['accuracy']:.1%}",
              help="Accuracy on the temporal hold-out set")
    c2.metric("AUC-ROC", f"{metrics['auc']:.3f}",
              help="Discrimination ability of the model (1 = perfect)")
    cv_label = (
        f"{metrics['cv_mean']:.3f} ± {metrics['cv_std']:.3f}"
        if not np.isnan(metrics["cv_mean"]) else "N/A"
    )
    c3.metric("CV AUC (temporal)", cv_label,
              help=f"TimeSeriesSplit with {N_CV_SPLITS} folds")
    c4.metric("Historical Retention", f"{metrics['retention_rate']:.1%}",
              help="% of employees who stayed in the training period")


def _render_feature_importance(feature_importance: pd.DataFrame) -> None:
    fig = px.bar(
        feature_importance,
        x="Importance",
        y="Feature",
        orientation="h",
        color="Importance",
        color_continuous_scale=[
            [0.0, PALETTE["light"]],
            [1.0, PALETTE["primary"]],
        ],
        labels={"Importance": "Feature Importance Score", "Feature": "Predictor"},
    )
    apply_default_layout(fig, "Retention Predictors — Feature Importance")
    fig.update_layout(
        height=400,
        coloraxis_showscale=False,
        xaxis=dict(gridcolor="#e0e0e0"),
    )
    st.plotly_chart(fig, use_container_width=True)


def _render_risk_calculator(model: Pipeline) -> None:
    st.subheader("6-Month Flight Risk Calculator")
    st.caption("Adjust the sliders to profile an employee and predict their departure probability.")

    col1, col2 = st.columns(2)
    with col1:
        tenure = st.slider("Tenure (months)", 1, 120, 24)
        salary_ratio = st.slider("Salary vs Market ratio", 0.80, 1.50, 1.00, 0.05)
        promo_days = st.slider("Days since last promotion", 0, 1095, 365)
        mgr_tenure = st.slider("Manager tenure (months)", 1, 60, 18)
    with col2:
        team_sz = st.slider("Team size", 3, 25, 8)
        neuro = st.selectbox("Neurodivergent", ["No", "Yes"])
        dept = st.selectbox("Department", list(DEPT_ENCODING.keys()))
        level = st.selectbox("Seniority level", list(LEVEL_ENCODING.keys()))

    input_df = pd.DataFrame([[
        tenure, salary_ratio, promo_days, mgr_tenure,
        team_sz, 1 if neuro == "Yes" else 0,
        DEPT_ENCODING[dept], LEVEL_ENCODING[level],
    ]], columns=SAFE_FEATURES)

    try:
        leave_prob = float(model.predict_proba(input_df)[0][1])
    except Exception:
        st.error("Prediction failed — please check input values.")
        return

    retention_prob = 1.0 - leave_prob
    st.metric("Predicted Retention Probability (6 months)", f"{retention_prob:.1%}")

    if leave_prob > 0.70:
        st.error("**HIGH RISK** — Immediate engagement action recommended.")
    elif leave_prob > 0.40:
        st.warning("**MODERATE RISK** — Proactive check-in advised.")
    else:
        st.success("**LOW RISK** — Employee likely to stay.")


def _render_model_save(model: Pipeline) -> None:
    if st.button("Save model to disk"):
        try:
            import joblib
            os.makedirs(MODEL_DIR, exist_ok=True)
            save_path = os.path.join(MODEL_DIR, "retention_model.joblib")
            joblib.dump(model, save_path)
            st.success(f"Model saved to `{save_path}`.")
        except ImportError:
            st.error("Install `joblib` to enable model saving.")
        except OSError as exc:
            st.error(f"Could not save model: {exc}")
