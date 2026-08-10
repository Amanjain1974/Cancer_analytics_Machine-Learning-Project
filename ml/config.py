from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "dataset" / "cancer_lifestyle_risk_dataset.csv"
MODEL_PATH = BASE_DIR / "models" / "model_pipeline.pkl"
RANDOM_STATE = 42

