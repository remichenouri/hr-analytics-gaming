import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def render_roi_calculator_improved(df_roi):
    st.header("💰 ROI Calculator - Retention & Diversity Programs")
    # SECTION 1: ML-Powered ROI Prediction
    st.subheader("🎯 ML-Powered ROI Prediction")
    col1, col2 = st.columns(2)
    with col1:
        st.info("**🤖 Modèle ML Integration**")
        high_risk_employees = st.number_input("Employés à haut risque (ML)", 20, 200, 75)
        medium_risk_employees = st.number_input("Employés à risque modéré (ML)", 50, 300, 120)
        model_accuracy = st.slider("Précision du modèle ML", 0.6, 0.95, 0.82, 0.01)
    with col2:
        st.info("**💼 Paramètres Entreprise**")
        company_size = st.number_input("Taille entreprise", 500, 5000, 1200)
        avg_salary = st.number_input("Salaire moyen (€)", 40000, 120000, 75000)
        current_turnover = st.slider("Taux turnover actuel (%)", 5, 30, 15)

    # SECTION 2: Program Parameters
    st.subheader("🎛️ Program Parameters")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**💰 Investissements**")
        program_investment = st.number_input("Investment programme (€)", 10000, 500000, 150000)
        cost_per_intervention = st.number_input("Coût par intervention (€)", 2000, 15000, 6000)
        implementation_months = st.slider("Durée implémentation (mois)", 3, 24, 12)
    with col2:
        st.write("**🎯 Efficacité Ciblage**")
        intervention_success_rate = st.slider("Taux succès intervention", 0.2, 0.8, 0.45, 0.05)
        targeting_precision = st.slider("Précision ciblage", 0.6, 0.95, 0.78, 0.01)
    with col3:
        st.write("**📊 Impact Différentiel**")
        neuro_retention_boost = st.slider("Boost rétention neurodivergents (%)", 5, 40, 18, 1)
        regular_retention_boost = st.slider("Boost rétention autres (%)", 3, 25, 12, 1)

    # SECTION 3: Calculs ROI
    multiplier = 1.8
    cost_per_departure = avg_salary * multiplier
    base_high = high_risk_employees * 0.75 * targeting_precision
    base_med = medium_risk_employees * 0.45 * targeting_precision
    total_base = base_high + base_med
    saved = total_base * intervention_success_rate
    total_savings = saved * cost_per_departure
    total_interventions = high_risk_employees + medium_risk_employees
    total_intervention_cost = total_interventions * cost_per_intervention
    total_program_cost = program_investment + total_intervention_cost
    net_roi = total_savings - total_program_cost
    roi_pct = (net_roi / total_program_cost) * 100 if total_program_cost > 0 else 0

    # SECTION 4: Résultats
    st.subheader("📊 ROI Analysis Results")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("💰 Économies Totales", f"€{total_savings:,.0f}", f"{saved:.0f} sauvés")
    m2.metric("📈 ROI Net (An 1)", f"€{net_roi:,.0f}", f"{roi_pct:.0f}%")
    months = (total_program_cost / (total_savings / 12)) if total_savings > 0 else float('inf')
    m3.metric("⏱️ Récupération", f"{months:.1f} mois" if months != float('inf') else "N/A", "Break-even")
    confidence = model_accuracy * targeting_precision * intervention_success_rate
    m4.metric("🎯 Score Confiance", f"{confidence:.1%}", "Fiabilité")

    # SECTION 5: Dashboard Interactif
    st.subheader("📊 Dashboard ROI Interactif")

    # 5.1 Bubble Chart
    col1, col2 = st.columns(2)
    with col1:
        scenarios = []
        for sr in np.arange(0.2, 0.8, 0.1):
            for pr in np.arange(0.6, 0.9, 0.05):
                base = (high_risk_employees * 0.75 + medium_risk_employees * 0.45) * pr
                saved_s = base * sr
                savings = saved_s * cost_per_departure
                roi = ((savings - total_program_cost) / total_program_cost) * 100
                scenarios.append({"sr": sr * 100, "pr": pr * 100, "roi": roi, "conf": sr * pr})
        df_s = pd.DataFrame(scenarios)
        fig_b = go.Figure(go.Scatter(
            x=df_s["sr"], y=df_s["pr"], mode="markers",
            marker=dict(size=df_s["roi"] / 5, color=df_s["roi"], colorscale="RdYlGn", showscale=True),
            text=[f"ROI : {r:.0f}%<br>Conf : {c:.1%}" for r, c in zip(df_s["roi"], df_s["conf"])],
            hovertemplate="%{x}% SR<br>%{y}% PR<br>%{text}<extra></extra>"
        ))
        fig_b.update_layout(title="🎯 Matrice ROI par Succès vs Précision",
                            xaxis_title="Taux Succès (%)", yaxis_title="Précision (%)", height=450)
        st.plotly_chart(fig_b, use_container_width=True)

    # 5.2 Waterfall Chart
    with col2:
        cats = ["Invest. Init.", "Coût Int.", "Économies", "ROI Net"]
        vals = [-program_investment, -total_intervention_cost, total_savings, net_roi]
        fig_w = go.Figure(go.Waterfall(
            orientation="v", measure=["relative"] * 3 + ["total"], x=cats, y=vals,
            text=[f"€{abs(v):,.0f}" for v in vals], textposition="outside",
            connector={"line": {"color": "#555"}}
        ))
        fig_w.update_layout(title="💰 Décomposition ROI - Waterfall", height=450)
        st.plotly_chart(fig_w, use_container_width=True)

    # 5.3 Heatmap
    st.subheader("🔥 Heatmap de Sensibilité ROI")
    srs = np.arange(0.2, 0.8, 0.05)
    prs = np.arange(0.6, 0.95, 0.02)
    heat = np.zeros((len(srs), len(prs)))
    for i, sr in enumerate(srs):
        for j, pr in enumerate(prs):
            base = (high_risk_employees * 0.75 + medium_risk_employees * 0.45) * pr
            saved_s = base * sr
            savings = saved_s * cost_per_departure
            heat[i, j] = ((savings - total_program_cost) / total_program_cost) * 100
    fig_h = go.Figure(go.Heatmap(
        z=heat, x=[f"{p:.0%}" for p in prs], y=[f"{s:.0%}" for s in srs],
        colorscale="RdYlGn", colorbar=dict(title="ROI %")
    ))
    fig_h.update_layout(title="🌡️ Heatmap ROI vs Paramètres",
                        xaxis_title="Précision", yaxis_title="Succès", height=400)
    st.plotly_chart(fig_h, use_container_width=True)

    # 5.4 Timeline ROI sur 5 ans
    st.subheader("📈 Évolution du ROI sur 5 ans")
    years = list(range(1, 6))
    cum = []
    for k, year in enumerate(years):
        factor = 0.9**k
        yearly = total_savings * factor
        value = yearly - total_program_cost if k == 0 else cum[-1] + yearly
        cum.append(value)
    fig_t = go.Figure(go.Scatter(x=years, y=cum, mode="lines+markers", fill="tonexty",
                                 line=dict(color="#667eea", width=3), marker=dict(size=8)))
    fig_t.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Break-even")
    fig_t.update_layout(title="🌎 ROI Cumulé sur 5 ans", xaxis_title="Années", yaxis_title="ROI (€)", height=400)
    st.plotly_chart(fig_t, use_container_width=True)

    # SECTION 6: Recommandations Stratégiques ML-Driven
    st.subheader("🎯 Recommandations Stratégiques ML-Driven")

    if roi_pct > 200:
        st.success("🚀 **ROI Exceptionnel** - Programme hautement rentable ! Déployez rapidement.")
        priority = "HAUTE"
    elif roi_pct > 100:
        st.info("💡 **ROI Solide** - Investissement judicieux avec retours mesurables.")
        priority = "MOYENNE"
    elif roi_pct > 0:
        st.warning("⚠️ **ROI Modéré** - Optimisez les paramètres avant déploiement.")
        priority = "FAIBLE"
    else:
        st.error("❌ **ROI Négatif** - Revisitez la stratégie d'intervention.")
        priority = "CRITIQUE"

    recommendations = [
        f"🎯 **Ciblage ML**: Le modèle identifie {high_risk_employees} employés prioritaires (précision {model_accuracy:.1%})",
        f"💰 **Budget Optimal**: {total_program_cost:,.0f}€ pour sauver ~{saved:.0f} employés",
        f"📊 **Monitoring**: Tracker mensuellement la rétention pour valider l'efficacité",
        f"🔄 **Itération**: Réentraîner le modèle tous les 6 mois avec nouvelles données",
        f"🎮 **Scaling Ubisoft**: Succès ici = expansion possible aux autres studios globalement"
    ]

    for i, rec in enumerate(recommendations, 1):
        st.info(f"**{i}.** {rec}")

    # Next Steps
    st.subheader("📋 Next Steps")
    if priority == "HAUTE":
        next_steps = [
            "✅ Valider le budget avec la direction",
            "🚀 Lancer le programme pilote sur 3 mois",
            "📊 Mettre en place le monitoring temps réel",
            "🎯 Former les équipes RH sur l'utilisation du modèle ML"
        ]
    elif priority == "MOYENNE":
        next_steps = [
            "🔧 Optimiser les paramètres d'intervention",
            "📊 Tester sur un échantillon réduit",
            "💡 Améliorer la précision du modèle ML",
            "📈 Ré-évaluer le ROI après ajustements"
        ]
    else:
        next_steps = [
            "🔍 Analyser les causes du ROI faible",
            "💰 Réviser les coûts d'intervention",
            "🎯 Améliorer l'efficacité du ciblage ML",
            "📊 Benchmarker avec d'autres approches"
        ]

    for step in next_steps:
        st.write(f"• {step}")

# Fonction de compatibilité
def render_roi_calculator(df_roi):
    return render_roi_calculator_improved(df_roi)
