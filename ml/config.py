from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "dataset" / "cancer_issue.csv"
MODEL_PATH = BASE_DIR / "models" / "model_pipeline.pkl"
RANDOM_STATE = 42
