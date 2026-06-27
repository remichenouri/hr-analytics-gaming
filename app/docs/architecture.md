# Architecture technique

## Vue d'ensemble

L'application Ubisoft People Analytics suit une architecture modulaire en couches pour assurer la scalabilité et la maintenabilité.

## Diagramme d'architecture

graph TB
subgraph "Frontend Layer"
A[Streamlit Dashboard]
B[Plotly Visualizations]
C[Custom CSS/JS]
end

subgraph "API Layer"
    D[FastAPI Router]
    E[Authentication Middleware]
    F[Validation Layer]
end

subgraph "Business Logic"
    G[ML Model Service]
    H[Data Processing Service]
    I[Recommendation Engine]
    J[Analytics Service]
end

subgraph "Data Layer"
    K[PostgreSQL Database]
    L[MLflow Model Store]
    M[File Storage]
end

subgraph "External Systems"
    N[HR Systems API]
    O[Authentication Provider]
    P[Monitoring Systems]
end

A --> D
D --> G
D --> H
G --> L
H --> K
I --> K
D --> N
E --> O
J --> P

## Composants principaux

### 1. Frontend - Streamlit Application

**Fichier principal** : `src/app.py`

**Responsabilités** :
- Interface utilisateur interactive
- Visualisations temps réel
- Upload et validation des données
- Export des rapports

**Technologies** :
- Streamlit 1.28+
- Plotly pour visualisations interactives  
- Custom CSS pour styling

### 2. API Layer - FastAPI

**Structure** :
src/api/
├── init.py
├── main.py # App FastAPI
├── auth.py # Authentification
├── models.py # Pydantic models
└── routes/
├── predict.py # Endpoints ML
├── data.py # Gestion données
└── analytics.py # Analytics

**Endpoints principaux** :
- `POST /api/v1/predict/neurodiversity` - Détection profils
- `GET /api/v1/analytics/dashboard` - Métriques dashboard
- `POST /api/v1/data/upload` - Upload données

### 3. ML Pipeline

**Architecture ML** :
class MLPipeline:
"""Pipeline ML pour détection neurodiversité"""

def __init__(self, config: MLConfig):
    self.preprocessor = DataPreprocessor(config)
    self.feature_engineer = FeatureEngineer(config) 
    self.model = self.load_model(config.model_path)
    
def predict(self, data: pd.DataFrame) -> PredictionResult:
    # 1. Preprocessing
    clean_data = self.preprocessor.transform(data)
    
    # 2. Feature engineering  
    features = self.feature_engineer.transform(clean_data)
    
    # 3. Prédiction
    predictions = self.model.predict_proba(features)
    
    # 4. Post-processing et explainabilité
    explanations = self.explain_predictions(features, predictions)
    
    return PredictionResult(
        predictions=predictions,
        explanations=explanations,
        confidence_scores=self.calculate_confidence(predictions)
    )

### 4. Data Layer

**Base de données PostgreSQL** :
-- Schema principal
CREATE SCHEMA hr_analytics;

-- Tables principales
CREATE TABLE hr_analytics.employees (
employee_id UUID PRIMARY KEY,
hire_date DATE,
department VARCHAR(50),
role VARCHAR(100),
performance_score FLOAT,
-- Données anonymisées
anonymized_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE hr_analytics.predictions (
prediction_id UUID PRIMARY KEY,
employee_id UUID REFERENCES hr_analytics.employees(employee_id),
model_version VARCHAR(20),
prediction_score FLOAT,
confidence_score FLOAT,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

## Patterns de conception utilisés

### 1. Repository Pattern
class EmployeeRepository:
"""Abstraction accès données employés"""

async def get_by_id(self, employee_id: UUID) -> Employee:
    pass
    
async def get_by_department(self, dept: str) -> List[Employee]:
    pass

### 2. Factory Pattern  
class ModelFactory:
"""Factory pour créer modèles ML selon configuration"""

text
@staticmethod
def create_model(model_type: str, config: dict) -> BaseModel:
    if model_type == "neurodiversity_detection":
        return NeurodiversityDetectionModel(config)
    elif model_type == "turnover_prediction":
        return TurnoverPredictionModel(config)

### 3. Observer Pattern
class ModelMonitor:
"""Monitoring performances modèles ML"""

def __init__(self):
    self.observers = []
    
def notify_prediction(self, prediction: PredictionResult):
    for observer in self.observers:
        observer.update(prediction)

## Configuration

**Structure de configuration** :
@dataclass
class AppConfig:
"""Configuration application"""
database_url: str
model_path: str
log_level: str = "INFO"
enable_monitoring: bool = True

@dataclass
class MLConfig:
"""Configuration modèles ML"""
model_type: str
hyperparameters: dict
feature_columns: List[str]
target_column: str

## Sécurité

### 1. Authentification JWT
async def verify_token(token: str = Depends(oauth2_scheme)):
try:
payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
username: str = payload.get("sub")
if username is None:
raise credentials_exception
except JWTError:
raise credentials_exception

### 2. Validation données
class EmployeeData(BaseModel):
"""Validation Pydantic données employés"""
employee_id: UUID
department: str = Field(..., min_length=1, max_length=50)
performance_score: float = Field(..., ge=0, le=10)

### 3. Anonymisation
def anonymize_employee_data(df: pd.DataFrame) -> pd.DataFrame:
"""Anonymise données personnelles"""
df['employee_id'] = df['employee_id'].apply(lambda x: hashlib.sha256(str(x).encode()).hexdigest())
df.drop(columns=['name', 'email', 'phone'], inplace=True)
return df

text

## Performance et scalabilité

### 1. Caching avec Redis
@lru_cache(maxsize=128)
def get_model_predictions(employee_data_hash: str):
"""Cache prédictions pour éviter recalculs"""
pass

### 2. Pagination API
@router.get("/employees")
async def get_employees(skip: int = 0, limit: int = 100):
"""Pagination pour grandes datasets"""
return db.get_employees(skip=skip, limit=limit)

### 3. Async processing
async def process_batch_predictions(employee_data: List[dict]):
"""Traitement asynchrone batch prédictions"""
tasks = [predict_employee(emp) for emp in employee_data]
return await asyncio.gather(*tasks)

## Monitoring et observabilité

### 1. Logs structurés
logger.info(
"Prediction completed",
extra={
"employee_count": len(data),
"model_version": model.version,
"processing_time_ms": processing_time,
"accuracy_score": accuracy
}
)

### 2. Métriques business
Prometheus metrics
PREDICTION_COUNTER = Counter('ml_predictions_total', 'Total ML predictions')
PREDICTION_DURATION = Histogram('ml_prediction_duration_seconds', 'ML prediction duration')
MODEL_ACCURACY = Gauge('ml_model_accuracy', 'Current model accuracy')

### 3. Health checks
@router.get("/health")
async def health_check():
"""Health check application"""
return {
"status": "healthy",
"database": await check_database_connection(),
"model": await check_model_availability(),
"timestamp": datetime.utcnow()
}

text

Cette architecture assure une séparation claire des responsabilités, une haute testabilité e
