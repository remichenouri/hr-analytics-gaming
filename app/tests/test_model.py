import pandas as pd, joblib
from sklearn.metrics import f1_score

DATA = "data/sample_data.csv"
MODEL = "models/random_forest.pkl"

def test_model_f1_threshold():
    df = pd.read_csv(DATA)
    X, y = df.drop(columns=["adhd_risk"]), df["adhd_risk"]
    clf = joblib.load(MODEL)
    f1 = f1_score(y, clf.predict(X))
    assert f1 >= 0.90, f"F1 too low ({f1:.2f})"
