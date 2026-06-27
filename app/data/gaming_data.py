"""Industry-level reference data and constants for the Gaming HR Analytics dashboard."""

import pandas as pd
import numpy as np

# ── Constants ──────────────────────────────────────────────────────────────────
_RNG = np.random.default_rng(42)

GAMING_ROLES = [
    "Game Developer", "Game Designer", "Technical Artist",
    "UI/UX Designer", "Quality Assurance", "Producer",
    "Community Manager", "Data Analyst", "DevOps Engineer",
    "Narrative Designer", "3D Artist", "Animator",
    "Sound Designer", "Marketing Specialist", "HR Specialist",
]

SKILLS_IN_DEMAND = [
    "Unity Development", "Unreal Engine", "Data Analytics",
    "AI/Machine Learning", "Cloud Gaming", "AR/VR Development",
    "Neurodiversity Awareness", "UX Research", "DevOps",
    "Community Management", "Live Operations", "Monetisation",
]


class GamingIndustryReferenceData:
    """Static reference data for a fictional multi-studio gaming organisation.

    All values are illustrative and generated synthetically.
    Not based on any real company's internal data.
    """

    STUDIOS: dict[str, dict] = {
        "HQ Paris":       {"employees": 400,  "focus": "R&D, Publishing"},
        "Studio Montreal":{"employees": 1_200, "focus": "AAA Development"},
        "Studio Toronto": {"employees": 800,  "focus": "Mobile, Live Services"},
        "Studio Barcelona":{"employees": 300, "focus": "Mobile Games"},
        "Studio Berlin":  {"employees": 200,  "focus": "Strategy Games"},
        "Studio San Jose":{"employees": 350,  "focus": "Technology, AI"},
        "Studio Warsaw":  {"employees": 600,  "focus": "Development Support"},
    }

    FRANCHISES: dict[str, dict] = {
        "Project Horizon": {"team_size": 800, "neurodiversity_correlation": 0.85, "creativity_score": 92},
        "Iron Protocol":   {"team_size": 600, "neurodiversity_correlation": 0.78, "creativity_score": 88},
        "Desert Frontier": {"team_size": 450, "neurodiversity_correlation": 0.82, "creativity_score": 90},
        "Rhythm Legends":  {"team_size": 200, "neurodiversity_correlation": 0.76, "creativity_score": 85},
        "Cipher City":     {"team_size": 350, "neurodiversity_correlation": 0.80, "creativity_score": 87},
    }

    COMPETITORS: list[str] = [
        "StudioAlpha", "CompanyBeta", "GroupGamma",
        "StudioDelta", "DevHouseEpsilon", "StudioZeta", "StudioEta",
    ]
    FOCAL = "StudioAlpha"

    def get_studio_demographics(self) -> pd.DataFrame:
        """Return monthly demographic snapshots for each studio (12 months)."""
        records = []
        for studio, info in self.STUDIOS.items():
            for month in range(1, 13):
                records.append({
                    "Studio": studio,
                    "Month": month,
                    "Employees": info["employees"] + int(_RNG.integers(-20, 51)),
                    "Neurodivergent_Percentage": float(_RNG.uniform(12, 22)),
                    "Gender_Diversity": float(_RNG.uniform(0.30, 0.50)),
                    "Age_Average": float(_RNG.uniform(28, 35)),
                    "Satisfaction_Score": float(_RNG.uniform(3.8, 4.5)),
                    "Innovation_Rating": float(_RNG.uniform(75, 95)),
                    "Focus_Area": info["focus"],
                })
        return pd.DataFrame(records)

    def get_franchise_performance(self) -> pd.DataFrame:
        """Return quarterly performance metrics per franchise."""
        records = []
        for franchise, metrics in self.FRANCHISES.items():
            for quarter in range(1, 5):
                base = float(metrics["creativity_score"])
                corr = float(metrics["neurodiversity_correlation"])
                records.append({
                    "Franchise": franchise,
                    "Quarter": f"Q{quarter} 2024",
                    "Team_Size": int(metrics["team_size"]) + int(_RNG.integers(-50, 101)),
                    "Creativity_Score": float(np.clip(base + _RNG.uniform(-5, 5), 70, 100)),
                    "Innovation_Index": float(np.clip(base * corr + _RNG.uniform(-10, 10), 50, 100)),
                    "User_Rating": float(np.clip(_RNG.uniform(7.5, 9.2), 1, 10)),
                    "Revenue_Impact_M": float(np.clip(_RNG.uniform(50, 200), 0, None)),
                    "Neurodiversity_Level": float(_RNG.uniform(15, 25)),
                    "Problem_Solving_Score": float(np.clip(_RNG.uniform(80, 95), 0, 100)),
                    "Collaboration_Rating": float(np.clip(_RNG.uniform(85, 98), 0, 100)),
                })
        return pd.DataFrame(records)

    def get_industry_benchmarks(self) -> pd.DataFrame:
        """Return cross-company HR benchmark data."""
        records = []
        for company in self.COMPETITORS:
            is_focal = company == self.FOCAL
            records.append({
                "Company": company,
                "Annual_Turnover_Rate": float(
                    _RNG.uniform(10, 15) if is_focal else _RNG.uniform(15, 25)
                ),
                "Employee_Satisfaction": float(
                    _RNG.uniform(4.0, 4.4) if is_focal else _RNG.uniform(3.5, 4.1)
                ),
                "Diversity_Index": float(
                    _RNG.uniform(0.68, 0.75) if is_focal else _RNG.uniform(0.55, 0.70)
                ),
                "Innovation_Score": float(
                    _RNG.uniform(85, 95) if is_focal else _RNG.uniform(70, 90)
                ),
                "Revenue_Billions": float(_RNG.uniform(1.5, 8.5)),
                "Employee_Count": int(_RNG.integers(2_000, 20_001)),
                "Has_Neurodiversity_Programme": bool(_RNG.choice([True, False], p=[0.3, 0.7])),
                "Remote_Work_Ratio": float(_RNG.uniform(0.3, 0.8)),
            })
        return pd.DataFrame(records)

    def get_skill_demand_trends(self) -> pd.DataFrame:
        """Return 24-month skill demand trends with monotonic growth for emerging skills."""
        months = pd.date_range(start="2023-01-01", periods=24, freq="ME")
        records = []
        for skill in SKILLS_IN_DEMAND:
            for i, month in enumerate(months):
                # Neurodiversity Awareness grows linearly from ~20 to ~65 over 24 months
                if "Neurodiversity" in skill:
                    base_demand = 20.0 + i * 1.9 + float(_RNG.uniform(-3, 5))
                else:
                    base_demand = float(_RNG.uniform(40, 90))
                records.append({
                    "Skill": skill,
                    "Month": month,
                    "Demand_Score": float(np.clip(base_demand, 0, 100)),
                    "Salary_Premium_Pct": float(np.clip(_RNG.uniform(0, 25), 0, 50)),
                    "Market_Availability": float(np.clip(_RNG.uniform(20, 80), 0, 100)),
                })
        return pd.DataFrame(records)


# ── Module-level helpers ───────────────────────────────────────────────────────

def get_gaming_industry_stats() -> dict[str, str]:
    """Return high-level gaming industry statistics (illustrative figures)."""
    return {
        "global_revenue_2024": "184.4 Billion USD",
        "gaming_workforce_growth": "8.2 % annually",
        "neurodivergent_population": "15–20 % (estimated)",
        "remote_work_adoption": "67 % post-COVID",
        "ai_adoption_rate": "45 % of studios",
        "diversity_investment": "2.3 Billion USD (2023–2024)",
    }


def get_roi_multipliers() -> dict[str, float]:
    """Return domain-specific ROI multipliers used in the calculator."""
    return {
        "creativity_boost": 1.8,
        "innovation_premium": 2.2,
        "retention_value": 1.5,
        "neurodiversity_multiplier": 1.25,
        "franchise_value_impact": 3.5,
        "user_engagement_correlation": 0.73,
    }
