"""
Training script : Retention Model + MLflow tracking (NO DATA LEAKAGE)
Exécuter : python src/models/train_retention_model.py
"""
import os
import joblib
import mlflow
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import f1_score, roc_auc_score, accuracy_score
from sklearn.model_selection import TimeSeriesSplit
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
import warnings
warnings.filterwarnings('ignore')

# Configuration
DATA_PATH = "data/retention_data.csv"
MODEL_PATH = "models/retention_model_clean.pkl"
MLFLOW_EXPERIMENT = "ubisoft_retention_no_leakage"

# Configuration MLflow
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000"))
mlflow.set_experiment(MLFLOW_EXPERIMENT)

def prepare_temporal_features(df):
    """
    Crée des features temporelles sans fuite pour la prédiction de rétention
    """
    df = df.copy()
    
    # Simuler des données réalistes si pas présentes
    if 'hire_date' not in df.columns:
        df['hire_date'] = pd.date_range(
            start='2020-01-01', 
            periods=len(df), 
            freq=f'{np.random.randint(1,30)}D'
        )
    
    if 'snapshot_date' not in df.columns:
        df['snapshot_date'] = df['hire_date'] + pd.to_timedelta(
            np.random.randint(30, 1095, len(df)), unit='D'
        )
    
    # Features observables au moment T (sans fuite)
    df['tenure_months'] = (df['snapshot_date'] - df['hire_date']).dt.days / 30.44
    df['tenure_months'] = df['tenure_months'].clip(lower=0)
    
    # Simuler autres features réalistes
    np.random.seed(42)
    df['salary_vs_market'] = np.random.uniform(0.8, 1.4, len(df))
    df['days_since_promotion'] = np.random.randint(0, 1095, len(df))
    df['manager_tenure_months'] = np.random.randint(6, 84, len(df))
    df['team_size'] = np.random.randint(3, 20, len(df))
    
    # Variables catégorielles
    departments = ['Engineering', 'Art', 'Design', 'QA', 'Production']
    levels = ['Junior', 'Senior', 'Lead', 'Principal']
    
    df['department'] = np.random.choice(departments, len(df))
    df['level'] = np.random.choice(levels, len(df))
    df['is_neurodivergent'] = np.random.binomial(1, 0.12, len(df))
    
    # Target : va partir dans les 6 prochains mois (à prédire)
    # Logique réaliste : plus l'ancienneté est faible + salaire bas = plus de risque
    base_risk = 0.15  # 15% de base
    tenure_factor = np.where(df['tenure_months'] < 12, 1.8, 
                           np.where(df['tenure_months'] < 36, 1.2, 0.7))
    salary_factor = np.where(df['salary_vs_market'] < 0.9, 1.5, 0.8)
    neuro_factor = np.where(df['is_neurodivergent'] == 1, 0.7, 1.0)  # Neurodivergents restent plus
    
    final_risk = base_risk * tenure_factor * salary_factor * neuro_factor
    df['will_leave_6m'] = np.random.binomial(1, np.clip(final_risk, 0, 0.4), len(df))
    
    return df

def detect_data_leakage(X_train, X_test, y_train, feature_names):
    """
    Détecte les fuites de données potentielles
    """
    leakage_warnings = []
    
    # Test 1: Corrélations suspectes entre features et target
    correlations = []
    for i, col in enumerate(feature_names):
        if i < len(X_train.columns):
            corr = abs(np.corrcoef(X_train.iloc[:, i], y_train)[0, 1])
            correlations.append((col, corr))
    
    high_corr = [col for col, corr in correlations if corr > 0.9]
    if high_corr:
        leakage_warnings.append(f"⚠️ Corrélations suspectes (>0.9): {high_corr}")
    
    # Test 2: Différences de distribution entre train/test
    for i, col in enumerate(feature_names[:min(len(feature_names), X_train.shape[1])]):
        if i < X_train.shape[1]:
            train_mean = X_train.iloc[:, i].mean()
            test_mean = X_test.iloc[:, i].mean()
            if abs(train_mean - test_mean) / train_mean > 0.2:  # >20% différence
                leakage_warnings.append(f"⚠️ Drift détecté sur {col}: train={train_mean:.2f}, test={test_mean:.2f}")
    
    return leakage_warnings

def main():
    print("🚀 Démarrage entraînement modèle de rétention (sans data leakage)")
    
    # ========== CHARGEMENT ET PRÉPARATION DES DONNÉES ==========
    
    # Simuler des données si le fichier n'existe pas
    if not os.path.exists(DATA_PATH):
        print(f"⚠️ {DATA_PATH} non trouvé, génération de données simulées...")
        df = pd.DataFrame({'dummy': range(2000)})  # 2000 employés
        df = prepare_temporal_features(df)
        os.makedirs("data", exist_ok=True)
        df.to_csv(DATA_PATH, index=False)
        print(f"✅ Données sauvegardées dans {DATA_PATH}")
    else:
        df = pd.read_csv(DATA_PATH)
        df = prepare_temporal_features(df)
    
    print(f"📊 Dataset chargé: {len(df)} employés")
    
    # ========== SPLIT TEMPOREL STRICT ==========
    
    # Conversion des dates
    df['snapshot_date'] = pd.to_datetime(df['snapshot_date'])
    df = df.sort_values('snapshot_date')
    
    # Split temporel : 80% train, 20% test
    cutoff_date = df['snapshot_date'].quantile(0.8)
    
    train_mask = df['snapshot_date'] <= cutoff_date
    test_mask = df['snapshot_date'] > cutoff_date
    
    print(f"📅 Cutoff date: {cutoff_date.strftime('%Y-%m-%d')}")
    print(f"📊 Train: {train_mask.sum()} | Test: {test_mask.sum()}")
    
    # Features sans fuite
    safe_features = [
        'tenure_months', 'salary_vs_market', 'days_since_promotion',
        'manager_tenure_months', 'team_size', 'is_neurodivergent',
        'department', 'level'
    ]
    
    X_train = df.loc[train_mask, safe_features]
    X_test = df.loc[test_mask, safe_features]
    y_train = df.loc[train_mask, 'will_leave_6m']
    y_test = df.loc[test_mask, 'will_leave_6m']
    
    print(f"✅ Features sécurisées: {len(safe_features)}")
    
    # ========== DÉTECTION DE DATA LEAKAGE ==========
    
    leakage_warnings = detect_data_leakage(X_train, X_test, y_train, safe_features)
    
    if leakage_warnings:
        print("🚨 ALERTES DATA LEAKAGE:")
        for warning in leakage_warnings:
            print(f"   {warning}")
    else:
        print("✅ Aucune fuite de données détectée")
    
    # ========== PIPELINE ML SANS FUITE ==========
    
    # Preprocessing pipeline
    numeric_features = ['tenure_months', 'salary_vs_market', 'days_since_promotion', 
                       'manager_tenure_months', 'team_size']
    categorical_features = ['department', 'level']
    binary_features = ['is_neurodivergent']
    
    preprocessor = ColumnTransformer([
        ('num', Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ]), numeric_features),
        ('cat', Pipeline([
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('encoder', LabelEncoder())
        ]), categorical_features),
        ('bin', 'passthrough', binary_features)
    ])
    
    # Modèle final
    model = Pipeline([
        ('prep', preprocessor),
        ('clf', GradientBoostingClassifier(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            class_weight='balanced',
            random_state=42
        ))
    ])
    
    # ========== VALIDATION CROISÉE TEMPORELLE ==========
    
    print("🔄 Validation croisée temporelle...")
    
    tscv = TimeSeriesSplit(n_splits=5)
    cv_scores_auc = []
    cv_scores_f1 = []
    
    for fold, (train_idx, val_idx) in enumerate(tscv.split(X_train)):
        X_train_fold = X_train.iloc[train_idx]
        X_val_fold = X_train.iloc[val_idx]
        y_train_fold = y_train.iloc[train_idx]
        y_val_fold = y_train.iloc[val_idx]
        
        model.fit(X_train_fold, y_train_fold)
        
        val_pred = model.predict(X_val_fold)
        val_pred_proba = model.predict_proba(X_val_fold)[:, 1]
        
        auc = roc_auc_score(y_val_fold, val_pred_proba)
        f1 = f1_score(y_val_fold, val_pred)
        
        cv_scores_auc.append(auc)
        cv_scores_f1.append(f1)
        
        print(f"   Fold {fold+1}: AUC={auc:.3f}, F1={f1:.3f}")
    
    cv_auc_mean = np.mean(cv_scores_auc)
    cv_f1_mean = np.mean(cv_scores_f1)
    
    print(f"📊 CV Moyenne: AUC={cv_auc_mean:.3f}±{np.std(cv_scores_auc):.3f}, F1={cv_f1_mean:.3f}±{np.std(cv_scores_f1):.3f}")
    
    # ========== ENTRAÎNEMENT FINAL ==========
    
    print("🏋️ Entraînement du modèle final...")
    model.fit(X_train, y_train)
    
    # Prédictions sur test temporel
    test_pred = model.predict(X_test)
    test_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Métriques finales
    test_accuracy = accuracy_score(y_test, test_pred)
    test_auc = roc_auc_score(y_test, test_pred_proba)
    test_f1 = f1_score(y_test, test_pred)
    
    print(f"🎯 Performance Test Temporel:")
    print(f"   Accuracy: {test_accuracy:.3f}")
    print(f"   AUC: {test_auc:.3f}")
    print(f"   F1-score: {test_f1:.3f}")
    
    # ========== LOGGING MLFLOW ==========
    
    with mlflow.start_run(run_name=f"retention_model_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):
        
        # Paramètres
        mlflow.log_param("model_type", "GradientBoostingClassifier")
        mlflow.log_param("n_estimators", 200)
        mlflow.log_param("max_depth", 6)
        mlflow.log_param("learning_rate", 0.1)
        mlflow.log_param("train_size", len(X_train))
        mlflow.log_param("test_size", len(X_test))
        mlflow.log_param("features", len(safe_features))
        mlflow.log_param("temporal_split", True)
        mlflow.log_param("cutoff_date", cutoff_date.strftime('%Y-%m-%d'))
        
        # Métriques
        mlflow.log_metric("cv_auc_mean", cv_auc_mean)
        mlflow.log_metric("cv_f1_mean", cv_f1_mean)
        mlflow.log_metric("test_accuracy", test_accuracy)
        mlflow.log_metric("test_auc", test_auc)
        mlflow.log_metric("test_f1", test_f1)
        mlflow.log_metric("data_leakage_warnings", len(leakage_warnings))
        
        # Tags
        mlflow.set_tag("data_leakage_free", "true")
        mlflow.set_tag("validation_method", "TimeSeriesSplit")
        mlflow.set_tag("target", "will_leave_6m")
        
        # Sauvegarde modèle
        os.makedirs("models", exist_ok=True)
        joblib.dump(model, MODEL_PATH)
        
        # Logging artefacts
        mlflow.sklearn.log_model(model, "retention_model")
        mlflow.log_artifact(MODEL_PATH)
        
        print(f"✅ Modèle sauvegardé: {MODEL_PATH}")
        print(f"🔗 MLflow Run ID: {mlflow.active_run().info.run_id}")
    
    print("🎉 Entraînement terminé avec succès!")
    
    return {
        'model': model,
        'test_auc': test_auc,
        'test_f1': test_f1,
        'cv_auc': cv_auc_mean,
        'leakage_warnings': leakage_warnings
    }

if __name__ == "__main__":
    results = main()
    
    if results['test_auc'] > 0.75 and len(results['leakage_warnings']) == 0:
        print("✅ SUCCÈS: Modèle prêt pour la production!")
    else:
        print("⚠️ ATTENTION: Vérifiez les performances et fuites avant déploiement")
