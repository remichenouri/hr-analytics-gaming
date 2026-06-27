from fastapi import FastAPI
from pydantic import BaseModel
import joblib, pandas as pd

app = FastAPI(
    title="Ubisoft People Analytics API",
    description="Endpoints prédiction / analytics",
    version="0.1.0",
)

MODEL = joblib.load("models/random_forest.pkl")


class EmployeeFeatures(BaseModel):
    creative_score: float
    burnout_scale: float
    hours_played_weekly: float
    department: str


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/predict")
def predict(item: EmployeeFeatures):
    df = pd.DataFrame([item.dict()])
    pred = MODEL.predict(df)[0]
    proba = MODEL.predict_proba(df)[0].tolist()
    return {"adhd_risk": int(pred), "probabilities": proba}
