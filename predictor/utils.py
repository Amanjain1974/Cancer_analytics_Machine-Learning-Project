import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "model_pipeline.pkl"

def load_model():
    return joblib.load(MODEL_PATH)
