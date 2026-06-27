"""
ETL helpers for Ubisoft People Analytics
---------------------------------------
Extract -> Transform -> Load pipeline vers PostgreSQL.
"""

import os
import pandas as pd
from sqlalchemy import create_engine

# URL sous forme postgresql://user:pwd@host:port/db
DB_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://etl:etl@localhost:5432/upa"
)
engine = create_engine(DB_URL, echo=False)


def extract(path: str) -> pd.DataFrame:
    """Lire un CSV brut et renvoyer un DataFrame."""
    return pd.read_csv(path)


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Nettoyage minimal + feature engineering."""
    df = df.copy()

    # Dé-duplication
    df.drop_duplicates(inplace=True)

    # Imputation basique
    df.fillna(method="ffill", inplace=True)

    # Exemple : normaliser une colonne catégorielle
    if "department" in df.columns:
        df["department"] = df["department"].str.lower()

    return df


def load(df: pd.DataFrame, table: str, if_exists: str = "append") -> None:
    """Charger le DataFrame dans PostgreSQL."""
    with engine.begin() as conn:
        df.to_sql(table, conn, if_exists=if_exists, index=False, method="multi")


if __name__ == "__main__":
    raw = extract("data/sample_data.csv")
    clean = transform(raw)
    load(clean, table="hr_employee_data", if_exists="replace")
