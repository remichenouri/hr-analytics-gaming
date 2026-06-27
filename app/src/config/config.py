"""
Configuration management for Ubisoft People Analytics
"""
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class DatabaseConfig:
    """Database configuration settings"""
    url: str = os.getenv("DATABASE_URL", "postgresql://localhost:5432/ubisoft_analytics")
    host: str = os.getenv("DB_HOST", "localhost")
    port: int = int(os.getenv("DB_PORT", "5432"))
    name: str = os.getenv("DB_NAME", "ubisoft_analytics")
    user: str = os.getenv("DB_USER", "postgres")
    password: str = os.getenv("DB_PASSWORD", "")
    pool_size: int = 10
    max_overflow: int = 20
    echo: bool = False


@dataclass
class MLConfig:
    """Machine Learning configuration"""
    model_path: str = os.getenv("MODEL_PATH", "models/")
    enable_monitoring: bool = os.getenv("ENABLE_MODEL_MONITORING", "true").lower() == "true"
    retrain_interval_days: int = int(os.getenv("MODEL_RETRAIN_INTERVAL", "7"))
    
    # Model parameters
    neurodiversity_threshold: float = 0.7
    turnover_threshold: float = 0.6
    confidence_threshold: float = 0.8
    
    # Feature engineering
    feature_columns: List[str] = field(default_factory=lambda: [
        "creativity_score", "technical_score", "focus_duration_min",
        "detail_orientation", "pattern_recognition", "sensory_sensitivity"
    ])
