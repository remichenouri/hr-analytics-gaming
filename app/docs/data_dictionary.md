# Dictionnaire des données

## Vue d'ensemble

Ce document décrit tous les datasets, tables et variables utilisés dans le projet Ubisoft People Analytics.

## 📊 Datasets principaux

### 1. Employee Demographics (`hr_analytics.employees`)

| Colonne | Type | Description | Exemple | Contraintes |
|---------|------|-------------|---------|-------------|
| `employee_id` | UUID | Identifiant unique anonymisé | `550e8400-e29b-41d4-a716-446655440000` | PRIMARY KEY, NOT NULL |
| `hire_date` | DATE | Date d'embauche | `2022-03-15` | NOT NULL, >= 2020-01-01 |
| `department` | VARCHAR(50) | Département/équipe | `Game Design`, `Programming`, `Art` | NOT NULL |
| `role` | VARCHAR(100) | Poste/fonction | `Senior Game Designer`, `Technical Artist` | NOT NULL |
| `seniority_level` | VARCHAR(20) | Niveau de séniorité | `Junior`, `Senior`, `Lead` | ENUM |
| `location` | VARCHAR(50) | Localisation bureau | `Montreal`, `Paris`, `Malmö` | NOT NULL |
| `employment_type` | VARCHAR(20) | Type de contrat | `Full-time`, `Contract`, `Intern` | NOT NULL |
| `created_at` | TIMESTAMP | Date de création record | `2025-09-11 10:30:00` | DEFAULT CURRENT_TIMESTAMP |
| `updated_at` | TIMESTAMP | Dernière modification | `2025-09-11 11:45:00` | AUTO UPDATE |

**Granularité** : Un enregistrement par employé  
**Historisation** : Oui, via champs temporels  
**Source** : Système SIRH (anonymisé)

### 2. Performance Metrics (`hr_analytics.performance`)

| Colonne | Type | Description | Exemple | Contraintes |
|---------|------|-------------|---------|-------------|
| `performance_id` | UUID | ID unique évaluation | `123e4567-e89b-12d3-a456-426614174000` | PRIMARY KEY |
| `employee_id` | UUID | Référence employé | `550e8400-e29b-41d4-a716-446655440000` | FOREIGN KEY |
| `evaluation_period` | VARCHAR(10) | Période d'évaluation | `2025-Q1`, `2024-H2` | NOT NULL |
| `overall_score` | DECIMAL(3,2) | Score global /10 | `7.85` | CHECK (0 <= score <= 10) |
| `creativity_score` | DECIMAL(3,2) | Score créativité | `8.20` | CHECK (0 <= score <= 10) |
| `technical_score` | DECIMAL(3,2) | Score technique | `7.10` | CHECK (0 <= score <= 10) |
| `collaboration_score` | DECIMAL(3,2) | Score collaboration | `6.90` | CHECK (0 <= score <= 10) |
| `innovation_projects` | INTEGER | Nb projets innovation | `3` | >= 0 |
| `patents_filed` | INTEGER | Brevets déposés | `1` | >= 0 |
| `peer_feedback_score` | DECIMAL(3,2) | Feedback pairs | `7.40` | CHECK (0 <= score <= 10) |
| `manager_rating` | DECIMAL(3,2) | Évaluation manager | `8.00` | CHECK (0 <= score <= 10) |

**Granularité** : Un enregistrement par employé par période  
**Fréquence** : Trimestrielle ou semestrielle  
**Source** : Outil d'évaluation performance interne

### 3. Behavioral Indicators (`hr_analytics.behavioral_data`)

| Colonne | Type | Description | Exemple | Contraintes |
|---------|------|-------------|---------|-------------|
| `behavior_id` | UUID | ID unique observation | `789e0123-e45b-67c8-d901-234567890abc` | PRIMARY KEY |
| `employee_id` | UUID | Référence employé | `550e8400-e29b-41d4-a716-446655440000` | FOREIGN KEY |
| `observation_date` | DATE | Date observation | `2025-09-10` | NOT NULL |
| `focus_duration_min` | INTEGER | Durée focus continu (min) | `120` | >= 0, <= 480 |
| `interruption_frequency` | INTEGER | Fréq. interruptions/jour | `15` | >= 0 |
| `communication_style` | VARCHAR(20) | Style communication | `Direct`, `Detailed`, `Visual` | ENUM |
| `workspace_preference` | VARCHAR(20) | Préférence espace travail | `Quiet`, `Collaborative`, `Flexible` | ENUM |
| `meeting_participation` | DECIMAL(3,2) | Score participation réunions | `6.50` | CHECK (0 <= score <= 10) |
| `detail_orientation` | DECIMAL(3,2) | Score attention détails | `9.20` | CHECK (0 <= score <= 10) |
| `pattern_recognition` | DECIMAL(3,2) | Score reconnaissance patterns | `8.70` | CHECK (0 <= score <= 10) |
| `routine_adherence` | DECIMAL(3,2) | Adhésion aux routines | `7.30` | CHECK (0 <= score <= 10) |
| `sensory_sensitivity` | VARCHAR(20) | Sensibilité sensorielle | `High`, `Medium`, `Low` | ENUM |

**Granularité** : Observations ponctuelles ou moyennes périodiques  
**Source** : Observations managériales + auto-évaluations (anonymisées)

### 4. ML Predictions (`hr_analytics.ml_predictions`)

| Colonne | Type | Description | Exemple | Contraintes |
|---------|------|-------------|---------|-------------|
| `prediction_id` | UUID | ID unique prédiction | `abc12345-def6-7890-ghij-123456789klm` | PRIMARY KEY |
| `employee_id` | UUID | Référence employé | `550e8400-e29b-41d4-a716-446655440000` | FOREIGN KEY |
| `model_name` | VARCHAR(50) | Nom du modèle | `neurodiversity_detector_v2.1` | NOT NULL |
| `model_version` | VARCHAR(20) | Version modèle | `v2.1.3` | NOT NULL |
| `prediction_type` | VARCHAR(30) | Type de prédiction | `neurodiversity_probability`, `turnover_risk` | NOT NULL |
| `prediction_value` | DECIMAL(5,4) | Valeur prédite | `0.7854` | CHECK (0 <= value <= 1) |
| `confidence_score` | DECIMAL(5,4) | Score de confiance | `0.9123` | CHECK (0 <= value <= 1) |
| `feature_importance` | JSON | Importance des features | `{"creativity": 0.25, "focus": 0.18}` | Valid JSON |
| `shap_values` | JSON | Valeurs SHAP explainabilité | `{"feature1": 0.12, "feature2": -0.05}` | Valid JSON |
| `prediction_date` | TIMESTAMP | Date de prédiction | `2025-09-11 14:20:00` | DEFAULT CURRENT_TIMESTAMP |
| `feedback_received` | BOOLEAN | Feedback reçu sur prédiction | `true` | DEFAULT false |
| `feedback_accuracy` | DECIMAL(3,2) | Précision selon feedback | `8.5` | CHECK (0 <= value <= 10) |

**Granularité** : Une prédiction par employé par modèle  
**Rétention** : 2 ans pour analyse longitudinale  
**Source** : Pipeline ML interne

## 📈 Features engineered

### Variables dérivées pour ML

| Feature | Description | Formule/Logique | Type |
|---------|-------------|-----------------|------|
| `neurodiversity_score` | Score composite neurodiversité | Weighted sum de 8 indicateurs comportementaux | FLOAT [0,1] |
| `creativity_potential` | Potentiel créatif estimé | `(creativity_score + innovation_projects * 0.3) / 10.3` | FLOAT [0,1] |
| `tenure_months` | Ancienneté en mois | `DATEDIFF(month, hire_date, CURRENT_DATE)` | INTEGER |
| `performance_trend` | Tendance performance | Régression linéaire 4 dernières évaluations | FLOAT [-1,1] |
| `collaboration_fit` | Fit équipe collaborative | Distance euclidienne aux profils équipe | FLOAT [0,1] |
| `sensory_accommodation_need` | Besoin aménagements | Règles business sur sensibilité sensorielle | CATEGORICAL |
| `focus_efficiency` | Efficacité concentration | `focus_duration_min / (interruption_frequency + 1)` | FLOAT |
| `communication_adaptability` | Adaptabilité communication | Variance styles selon contexte | FLOAT [0,1] |

## 🔒 Anonymisation et conformité

### Données personnelles supprimées
- Noms, prénoms
- Adresses email personnelles  
- Numéros de téléphone
- Adresses domicile
- Données médicales directes
- Photos de profil

### Méthodes d'anonymisation
1. **Hachage cryptographique** : ID employés via SHA-256
2. **Généralisation** : Âges → tranches d'âge, salaires → déciles
3. **Suppression** : Données non nécessaires à l'analyse
4. **Perturbation** : Ajout bruit statistique sur métriques sensibles
5. **Pseudonymisation** : Remplacement noms par codes anonymes

### Niveaux de sensibilité

| Niveau | Données | Accès | Rétention |
|--------|---------|-------|-----------|
| **Public** | Statistiques agrégées | Tous utilisateurs | Permanent |
| **Interne** | Métriques départementales | Équipe RH/Analytics | 3 ans |
| **Confidentiel** | Prédictions individuelles | Lead Data + RH Senior | 2 ans |
| **Restreint** | Données comportementales | Data Analyst certifié + audit | 1 an |

## 🎯 Cas d'usage par dataset

### Dashboard Executive
- **Tables** : `employees`, `performance`, `ml_predictions`  
- **Agrégations** : Moyennes par département, tendances temporelles
- **Métriques** : Turnover, satisfaction, scores innovation

### Détection Neurodiversité  
- **Tables** : `behavioral_data`, `performance`, `ml_predictions`
- **Features** : Tous indicateurs comportementaux + performance
- **Output** : Probabilité neurodiversité + explications SHAP

### Recommandations RH
- **Tables** : `ml_predictions`, `employees`, `behavioral_data`
- **Logique** : Matching profils + règles business accommodation
- **Output** : Actions personnalisées par employé

### Analyse ROI
- **Tables** : `performance`, `employees` (historique)
- **Calculs** : Impact performance avant/après accommodations
- **Métriques** : €€ économisés, gains productivité, rétention

---

*Dernière mise à jour : 11 septembre 2025*  
*Contact data : chenouri.remi@proton.me*
