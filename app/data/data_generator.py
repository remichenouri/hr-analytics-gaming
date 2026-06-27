"""Synthetic data generator for the Gaming Industry HR Analytics dashboard."""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ── Constants ──────────────────────────────────────────────────────────────────
RANDOM_SEED = 42

COMPANIES = ["StudioAlpha", "StudioBeta", "StudioGamma", "StudioDelta", "StudioEpsilon"]

# Focal company displayed as the benchmark in comparisons
FOCAL_COMPANY = COMPANIES[0]

DEPARTMENTS = ["Game Dev", "Art", "QA", "Marketing", "HR", "Engineering", "Design"]

# Turnover rates (annualised %)
FOCAL_TURNOVER_MEAN, FOCAL_TURNOVER_STD = 12.0, 2.0
INDUSTRY_TURNOVER_MEAN, INDUSTRY_TURNOVER_STD = 18.0, 3.0
TURNOVER_MIN, TURNOVER_MAX = 5.0, 30.0

# Satisfaction scores (1–5 Likert)
FOCAL_SATISFACTION_MEAN, FOCAL_SATISFACTION_STD = 4.2, 0.3
INDUSTRY_SATISFACTION_MEAN, INDUSTRY_SATISFACTION_STD = 3.8, 0.4
SATISFACTION_MIN, SATISFACTION_MAX = 1.0, 5.0

# Diversity index (0–1)
FOCAL_DIVERSITY_MEAN, FOCAL_DIVERSITY_STD = 0.72, 0.05
INDUSTRY_DIVERSITY_MEAN, INDUSTRY_DIVERSITY_STD = 0.65, 0.08
DIVERSITY_MIN, DIVERSITY_MAX = 0.40, 1.0

# Neurodiversity prevalence
NEURODIVERGENT_PREVALENCE = 0.15
N_EMPLOYEES = 1_000

# Cost multiplier: replacement cost = salary × REPLACEMENT_MULTIPLIER
REPLACEMENT_MULTIPLIER = 1.5


class GamingIndustryDataGenerator:
    """Generates reproducible synthetic HR datasets for a fictional gaming organisation."""

    def __init__(self, seed: int = RANDOM_SEED) -> None:
        self._rng = np.random.default_rng(seed)

    # ── Public generators ──────────────────────────────────────────────────────

    def generate_workforce_data(self) -> pd.DataFrame:
        """Return monthly workforce KPIs for each fictional studio (12 months)."""
        records = []
        for company in COMPANIES:
            is_focal = company == FOCAL_COMPANY
            turnover = self._rng.normal(
                FOCAL_TURNOVER_MEAN if is_focal else INDUSTRY_TURNOVER_MEAN,
                FOCAL_TURNOVER_STD if is_focal else INDUSTRY_TURNOVER_STD,
                12,
            )
            satisfaction = self._rng.normal(
                FOCAL_SATISFACTION_MEAN if is_focal else INDUSTRY_SATISFACTION_MEAN,
                FOCAL_SATISFACTION_STD if is_focal else INDUSTRY_SATISFACTION_STD,
                12,
            )
            diversity = self._rng.normal(
                FOCAL_DIVERSITY_MEAN if is_focal else INDUSTRY_DIVERSITY_MEAN,
                FOCAL_DIVERSITY_STD if is_focal else INDUSTRY_DIVERSITY_STD,
                12,
            )
            headcount_range = (800, 1_500) if is_focal else (600, 2_000)

            for month in range(12):
                records.append({
                    "Company": company,
                    "Month": month + 1,
                    "Turnover_Rate": float(
                        np.clip(turnover[month], TURNOVER_MIN, TURNOVER_MAX)
                    ),
                    "Employee_Satisfaction": float(
                        np.clip(satisfaction[month], SATISFACTION_MIN, SATISFACTION_MAX)
                    ),
                    "Diversity_Score": float(
                        np.clip(diversity[month], DIVERSITY_MIN, DIVERSITY_MAX)
                    ),
                    "Headcount": int(
                        self._rng.integers(*headcount_range)
                    ),
                })
        return pd.DataFrame(records)

    def generate_neurodiversity_data(self) -> pd.DataFrame:
        """Return simulated correlation between neurodiversity level and performance metrics."""
        levels = np.arange(0.05, 0.26, 0.01)  # 5 % → 25 %
        records = []
        for level in levels:
            innovation = 60.0 + level * 100.0 * 0.8 + float(self._rng.normal(0, 5))
            creativity = 0.60 + level * 1.5 + float(self._rng.normal(0, 0.1))
            problem_solving = 70.0 + level * 80.0 + float(self._rng.normal(0, 8))
            team_perf = 70.0 + level * 120.0 + float(self._rng.normal(0, 6))
            records.append({
                "Neurodiversity_Percentage": round(level * 100, 2),
                "Innovation_Score": float(np.clip(innovation, 50, 100)),
                "Creativity_Index": float(np.clip(creativity, 0.3, 1.5)),
                "Problem_Solving_Score": float(np.clip(problem_solving, 60, 100)),
                "Team_Performance": float(np.clip(team_perf, 65, 95)),
            })
        return pd.DataFrame(records)

    def generate_retention_data(self) -> pd.DataFrame:
        """Return employee-level features and a synthetic attrition label (N=1 000)."""
        rng = self._rng
        salary_pct = rng.uniform(20, 95, N_EMPLOYEES)
        wlb = rng.uniform(1, 5, N_EMPLOYEES)
        career = rng.uniform(1, 5, N_EMPLOYEES)
        manager = rng.uniform(1, 5, N_EMPLOYEES)
        neuro = rng.choice([0, 1], N_EMPLOYEES, p=[1 - NEURODIVERGENT_PREVALENCE, NEURODIVERGENT_PREVALENCE])

        retention_score = (
            salary_pct * 0.30
            + wlb * 15.0
            + career * 20.0
            + manager * 18.0
            + neuro * 25.0
            + rng.normal(0, 10, N_EMPLOYEES)
        )

        return pd.DataFrame({
            "Employee_ID": [f"EMP_{i:04d}" for i in range(N_EMPLOYEES)],
            "Salary_Percentile": salary_pct.round(1),
            "Work_Life_Balance": wlb.round(2),
            "Career_Growth": career.round(2),
            "Manager_Quality": manager.round(2),
            "Is_Neurodivergent": neuro,
            "Retention_Score": np.clip(retention_score, 0, 100).round(1),
            "Stayed": (retention_score > 70).astype(int),
            "Department": rng.choice(DEPARTMENTS, N_EMPLOYEES),
        })

    def generate_roi_data(self) -> pd.DataFrame:
        """Return cost/benefit estimates for six fictional HR programmes."""
        programmes = [
            "Neurodiversity Hiring Initiative",
            "Flexible Work Arrangements",
            "Manager Training Programme",
            "Employee Resource Groups",
            "Mental Health Support",
            "Inclusive Design Workshops",
        ]
        records = []
        for prog in programmes:
            is_neuro = "neurodiversity" in prog.lower()
            impl_cost = self._rng.uniform(50_000, 200_000)
            annual_cost = self._rng.uniform(20_000, 100_000)
            retention_gain = self._rng.uniform(25, 35) if is_neuro else self._rng.uniform(10, 20)
            productivity_gain = self._rng.uniform(18, 28) if is_neuro else self._rng.uniform(8, 15)
            innovation_boost = self._rng.uniform(20, 30) if is_neuro else self._rng.uniform(5, 15)
            records.append({
                "Programme": prog,
                "Implementation_Cost": round(float(impl_cost), 2),
                "Annual_Cost": round(float(annual_cost), 2),
                "Retention_Improvement_Percent": round(float(retention_gain), 2),
                "Productivity_Gain_Percent": round(float(productivity_gain), 2),
                "Innovation_Boost_Percent": round(float(innovation_boost), 2),
                "Employee_Satisfaction_Increase": round(float(self._rng.uniform(0.3, 0.8)), 2),
            })
        return pd.DataFrame(records)
