import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
import plotly.graph_objects as go
from datetime import datetime, timedelta
import joblib
import numpy as np

def render_retention_models(df_retention):
    st.header("📈 Talent Retention Predictive Models (No Data Leakage)")
    
    # ============ ÉTAPE 1: NETTOYAGE ET FEATURES ENGINEERING ============
    
    # Créer des features temporelles robustes (observables au moment T)
    df_clean = prepare_retention_features(df_retention.copy())
    
    # ============ ÉTAPE 2: SPLIT TEMPOREL STRICT ============
    
    # Supposons une colonne 'hire_date' ou 'snapshot_date'
    if 'snapshot_date' not in df_clean.columns:
        # Créer une date de snapshot simulée pour la demo
        df_clean['snapshot_date'] = pd.date_range(
            start='2022-01-01', 
            periods=len(df_clean), 
            freq='D'
        )
    
    # Split temporel : 80% train, 20% test
    cutoff_date = df_clean['snapshot_date'].quantile(0.8)
    
    train_mask = df_clean['snapshot_date'] <= cutoff_date
    test_mask = df_clean['snapshot_date'] > cutoff_date
    
    # Features sans fuite (observables au moment T)
    safe_features = [
        'tenure_months',           # Ancienneté au moment T
        'salary_vs_market',        # Ratio salaire/marché au moment T
        'days_since_promotion',    # Jours depuis dernière promotion
        'manager_tenure_months',   # Ancienneté du manager
        'team_size',              # Taille équipe
        'is_neurodivergent',      # Caractéristique stable
        'department_encoded',     # Département
        'level_encoded'           # Niveau hiérarchique
    ]
    
    X_train = df_clean.loc[train_mask, safe_features]
    X_test = df_clean.loc[test_mask, safe_features]
    y_train = df_clean.loc[train_mask, 'will_leave_6m']  # Target: partira dans 6 mois
    y_test = df_clean.loc[test_mask, 'will_leave_6m']
    
    st.info(f"📊 **Données d'entraînement**: {len(X_train)} employés | **Test temporel**: {len(X_test)} employés")
    
    # ============ ÉTAPE 3: PIPELINE ML SANS FUITE ============
    
    # Pipeline avec preprocessing intégré
    preprocessor = ColumnTransformer([
        ('num', StandardScaler(), ['tenure_months', 'salary_vs_market', 'days_since_promotion', 
                                  'manager_tenure_months', 'team_size']),
        ('cat', 'passthrough', ['is_neurodivergent', 'department_encoded', 'level_encoded'])
    ])
    
    model = Pipeline([
        ('prep', preprocessor),
        ('clf', GradientBoostingClassifier(
            n_estimators=100,
            max_depth=4,
            learning_rate=0.1,
            random_state=42
        ))
    ])
    
    # ============ ÉTAPE 4: ENTRAÎNEMENT ET VALIDATION ============
    
    model.fit(X_train, y_train)
    
    # Prédictions sur test temporel
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Métriques robustes
    accuracy = accuracy_score(y_test, y_pred)
    auc_score = roc_auc_score(y_test, y_pred_proba)
    
    # Validation croisée temporelle
    tscv = TimeSeriesSplit(n_splits=3)
    cv_scores = []
    for train_idx, val_idx in tscv.split(X_train):
        model.fit(X_train.iloc[train_idx], y_train.iloc[train_idx])
        val_pred = model.predict_proba(X_train.iloc[val_idx])[:, 1]
        cv_scores.append(roc_auc_score(y_train.iloc[val_idx], val_pred))
    
    cv_mean = np.mean(cv_scores)
    cv_std = np.std(cv_scores)
    
    # ============ ÉTAPE 5: AFFICHAGE DES RÉSULTATS ============
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🎯 Test Accuracy", f"{accuracy:.1%}", 
                 help="Performance sur données temporelles hold-out")
    
    with col2:
        st.metric("📈 AUC Score", f"{auc_score:.3f}", 
                 help="Capacité de discrimination du modèle")
    
    with col3:
        st.metric("🔄 CV Score", f"{cv_mean:.3f} ± {cv_std:.3f}", 
                 help="Validation croisée temporelle")
    
    with col4:
        retention_rate = 1 - y_train.mean()
        st.metric("📊 Retention Rate", f"{retention_rate:.1%}", 
                 help="Taux de rétention historique")
    
    # Feature Importance (sans fuite)
    feature_importance = pd.DataFrame({
        'Feature': safe_features,
        'Importance': model.named_steps['clf'].feature_importances_
    }).sort_values('Importance', ascending=True)
    
    fig_importance = px.bar(
        feature_importance,
        x='Importance',
        y='Feature',
        orientation='h',
        title="🔍 Facteurs de Rétention - Importance des Variables (Sans Fuite)",
        labels={'Importance': 'Score d\'Importance', 'Feature': 'Variables'}
    )
    fig_importance.update_layout(height=400)
    st.plotly_chart(fig_importance, use_container_width=True)
    
    # ============ ÉTAPE 6: CALCULATEUR DE RISQUE SÉCURISÉ ============
    
    st.subheader("🎯 Calculateur de Risque de Départ (6 mois)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        tenure_input = st.slider("Ancienneté (mois)", 1, 120, 24)
        salary_ratio = st.slider("Salaire vs Marché", 0.8, 1.5, 1.0, 0.05)
        promo_days = st.slider("Jours depuis promotion", 0, 1095, 365)
        manager_tenure = st.slider("Ancienneté manager (mois)", 1, 60, 18)
    
    with col2:
        team_size_input = st.slider("Taille équipe", 3, 25, 8)
        neuro_input = st.selectbox("Neurodivergent", ["Non", "Oui"])
        dept_input = st.selectbox("Département", ["Engineering", "Art", "Design", "QA", "Production"])
        level_input = st.selectbox("Niveau", ["Junior", "Senior", "Lead", "Principal"])
    
    # Encodage des variables catégorielles (à adapter selon vos données)
    dept_encoding = {"Engineering": 1, "Art": 2, "Design": 3, "QA": 4, "Production": 5}
    level_encoding = {"Junior": 1, "Senior": 2, "Lead": 3, "Principal": 4}
    
    # Prédiction en temps réel
    prediction_input = pd.DataFrame([[
        tenure_input, salary_ratio, promo_days, manager_tenure, 
        team_size_input, 1 if neuro_input == "Oui" else 0,
        dept_encoding[dept_input], level_encoding[level_input]
    ]], columns=safe_features)
    
    leave_proba = model.predict_proba(prediction_input)[0][1]
    retention_prob = 1 - leave_proba
    
    st.metric("🎯 Probabilité de Rétention", f"{retention_prob:.1%}", 
             "Likelihood de rester 6 mois")
    
    if leave_proba > 0.7:
        st.error("🚨 **RISQUE ÉLEVÉ** - Intervention immédiate recommandée")
    elif leave_proba > 0.4:
        st.warning("⚡ **RISQUE MODÉRÉ** - Surveillance renforcée")
    else:
        st.success("✅ **FAIBLE RISQUE** - Employé susceptible de rester")
    
    # ============ ÉTAPE 7: SAUVEGARDE DU MODÈLE ============
    
    if st.button("💾 Sauvegarder le modèle"):
        joblib.dump(model, 'models/retention_model_clean.joblib')
        st.success("Modèle sauvegardé dans models/retention_model_clean.joblib")

def prepare_retention_features(df):
    """
    Prépare des features sans fuite pour la prédiction de rétention
    """
    # Simuler des features temporelles réalistes (à adapter à vos vraies données)
    
    # Ancienneté en mois (observable)
    df['tenure_months'] = np.random.randint(1, 120, len(df))
    
    # Ratio salaire vs marché (observable au moment T)
    df['salary_vs_market'] = np.random.uniform(0.8, 1.4, len(df))
    
    # Jours depuis dernière promotion (observable)
    df['days_since_promotion'] = np.random.randint(0, 1095, len(df))
    
    # Ancienneté du manager (observable)
    df['manager_tenure_months'] = np.random.randint(6, 84, len(df))
    
    # Taille de l'équipe (observable)
    df['team_size'] = np.random.randint(3, 20, len(df))
    
    # Variables catégorielles encodées
    df['department_encoded'] = np.random.randint(1, 6, len(df))
    df['level_encoded'] = np.random.randint(1, 5, len(df))
    
    # Target : va partir dans les 6 prochains mois (à prédire)
    df['will_leave_6m'] = np.random.binomial(1, 0.15, len(df))  # 15% de turnover
    
    # Remplacer 'Is_Neurodivergent' par 'is_neurodivergent' (convention snake_case)
    if 'Is_Neurodivergent' in df.columns:
        df['is_neurodivergent'] = df['Is_Neurodivergent']
    else:
        df['is_neurodivergent'] = np.random.binomial(1, 0.12, len(df))  # 12% neurodivergents
    
    return df
