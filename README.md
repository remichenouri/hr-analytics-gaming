# 🇫🇷 ADHD Observatory — France

*Epidemiological analysis of ADHD in France using national health data*

[![Live App](https://img.shields.io/badge/App-Live-brightgreen)](https://observatoire-tdah-france.streamlit.app/)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-brightred)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## Overview

An interactive Streamlit dashboard for exploring trends in ADHD diagnosis and medication in France (2018–2024), built on open public health data.

Covers prescription volumes, regional disparities, demographic breakdowns, and longitudinal trends — with export capabilities for further analysis.

**Data sources**: Open Medic (reimbursed prescriptions), Cartographie des pathologies CNAM, Medic'AM — all publicly available from [data.ameli.fr](https://data.ameli.fr) and [data.gouv.fr](https://data.gouv.fr).

---

## Features

- 📊 **Dynamic dashboards** — prescription volumes and trends (2018–2024)
- 🗺️ **Regional breakdown** — geographic disparities across French departments
- 🔍 **Filters** — by region, treatment type, period, age group
- 📈 **Interactive charts** — time series, maps, histograms (Plotly)
- 📥 **Data export** — CSV/Excel download for further analysis
- 📄 **Automated reports** — PDF and Power BI outputs

---

## Repository structure

```
observatoire-tdah-france/
├── data/              # Raw and cleaned datasets
│   └── prescriptions_2018_2024.csv
├── notebooks/         # Exploratory Jupyter notebooks
├── scripts/           # Ingestion and transformation scripts
├── src/               # Reusable Python modules
├── streamlit-app/     # Streamlit application
│   ├── main.py
│   └── requirements.txt
├── power bi/          # Power BI dashboard files (.pbix)
├── reports/           # Generated reports (PDF, HTML)
├── tests/             # Unit tests
└── requirements.txt
```

---

## Getting started

```bash
git clone https://github.com/remichenouri/observatoire-tdah-france.git
cd observatoire-tdah-france
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit-app/main.py
```

---

## Tech stack

`Python 3.9+` · `Streamlit` · `pandas` · `NumPy` · `Plotly` · `scikit-learn` · `Power BI` · `pytest`

---

## Use cases

- **Researchers & data scientists** — longitudinal trend analysis and predictive modelling
- **Healthcare analysts** — regional prescription benchmarking
- **Policy analysts** — evaluating geographic disparities and healthcare access

---

## Contact

**Rémi Chenouri** — Commercial Excellence Data Analyst | Healthcare  
📧 chenouri.remi@proton.me · [LinkedIn](https://linkedin.com/in/remi-chenouri)

---

*Built with open data — Observatoire TDAH France is a portfolio project for data analysis and visualisation in public health.*
