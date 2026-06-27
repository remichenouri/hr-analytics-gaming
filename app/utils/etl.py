"""
ETL helpers for the Gaming Industry HR Analytics pipeline.

Extract → Transform → Load into a PostgreSQL database.
The database engine is created lazily so that importing this module
never raises a connection error in environments without a live DB.
"""

import logging
import os
from typing import Optional

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)

# ── Config ─────────────────────────────────────────────────────────────────────
_DB_URL: str = os.getenv(
    "DATABASE_URL",
    "postgresql://etl:etl@localhost:5432/hr_gaming",
)
_engine: Optional[Engine] = None


def _get_engine() -> Engine:
    """Return a cached SQLAlchemy engine, creating it on first call."""
    global _engine
    if _engine is None:
        _engine = create_engine(_DB_URL, echo=False, future=True)
    return _engine


# ── Pipeline steps ─────────────────────────────────────────────────────────────

def extract(path: str) -> pd.DataFrame:
    """Read a raw CSV file and return a DataFrame.

    Args:
        path: Absolute or relative path to the CSV file.

    Returns:
        Raw DataFrame.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If the file is empty or cannot be parsed.
    """
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        logger.error("CSV file not found: %s", path)
        raise
    except Exception as exc:
        logger.error("Failed to read CSV %s: %s", path, exc)
        raise ValueError(f"Cannot parse file '{path}': {exc}") from exc

    if df.empty:
        raise ValueError(f"File '{path}' is empty.")

    logger.info("Extracted %d rows from '%s'.", len(df), path)
    return df


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and lightly engineer a raw HR DataFrame.

    Steps:
    - Remove exact duplicate rows.
    - Forward-fill missing values within each column.
    - Lowercase the 'department' column if present.

    Args:
        df: Raw DataFrame from :func:`extract`.

    Returns:
        Cleaned DataFrame (copy, original is not mutated).
    """
    if df.empty:
        logger.warning("transform() received an empty DataFrame — returning as-is.")
        return df.copy()

    df = df.copy()

    before = len(df)
    df = df.drop_duplicates()
    dropped = before - len(df)
    if dropped:
        logger.info("Removed %d duplicate rows.", dropped)

    # pandas ≥ 2.2 deprecates fillna(method=); use ffill() instead
    df = df.ffill()

    if "department" in df.columns:
        df["department"] = df["department"].str.strip().str.lower()

    logger.info("Transform complete: %d rows remain.", len(df))
    return df


def load(df: pd.DataFrame, table: str, if_exists: str = "append") -> None:
    """Write a DataFrame to a PostgreSQL table.

    Args:
        df: Cleaned DataFrame to load.
        table: Target table name.
        if_exists: One of 'append', 'replace', 'fail' (passed to ``to_sql``).

    Raises:
        RuntimeError: If the database write fails.
    """
    if df.empty:
        logger.warning("load() called with empty DataFrame — skipping write to '%s'.", table)
        return

    try:
        engine = _get_engine()
        with engine.begin() as conn:
            df.to_sql(table, conn, if_exists=if_exists, index=False, method="multi")
        logger.info("Loaded %d rows into table '%s'.", len(df), table)
    except Exception as exc:
        logger.error("Failed to load data into '%s': %s", table, exc)
        raise RuntimeError(f"Database write to '{table}' failed: {exc}") from exc


# ── CLI entry-point ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    raw = extract("data/sample_data.csv")
    clean = transform(raw)
    load(clean, table="hr_employee_data", if_exists="replace")
