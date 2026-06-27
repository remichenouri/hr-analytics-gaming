# HR Analytics — Gaming Industry

*Workforce planning & diversity KPIs for the gaming industry — portfolio case study using synthetic data.*

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-brightred)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> **Disclaimer:** This is a portfolio project. All data is synthetic. Not affiliated with any company.

---

## Overview

An interactive Streamlit dashboard for HR analytics in the gaming industry — workforce planning, diversity KPIs, salary benchmarking, and attrition modeling.

Built as a portfolio case study to demonstrate applied HR analytics techniques using Python, SQL, and interactive visualization.

---

## Features

- 📊 **Workforce dashboard** — headcount trends, department breakdown, seniority distribution
- 🎯 **Diversity KPIs** — gender, seniority, and team composition tracking
- 💰 **Salary analysis** — compensation distribution by role and region
- 📉 **Attrition modeling** — churn risk scoring with feature importance (SHAP)
- 🔍 **Interactive filters** — by studio, role, region, and time period

---

## Repository structure

```
hr-analytics-gaming/
├── app.py                  # Main Streamlit application
├── src/
│   ├── data_loader.py      # Synthetic data generation
│   ├── kpi_engine.py       # KPI computation logic
│   └── viz.py              # Chart helpers (Plotly)
├── data/
│   └── synthetic/          # Auto-generated on first run
├── requirements.txt
└── README.md
```

---

## Getting started

```bash
git clone https://github.com/remichenouri/hr-analytics-gaming.git
cd hr-analytics-gaming
pip install -r requirements.txt
streamlit run app.py
```

---

## Tech stack

`Python 3.9+` · `Streamlit` · `pandas` · `Plotly` · `scikit-learn` · `SHAP` · `SQL`

---

## Use cases

- **HR analysts** — tracking workforce diversity and compensation equity
- **Data analysts** — exploring HR analytics techniques on a realistic synthetic dataset
- **Portfolio** — demonstrates applied analytics in a domain-specific context

---

## Contact

**Rémi Chenouri** — Healthcare Data Analyst | Commercial Performance  
📧 chenouri.remi@proton.me · [LinkedIn](https://linkedin.com/in/remi-chenouri)

---

*Portfolio project — synthetic data only. Not affiliated with any gaming company.*
