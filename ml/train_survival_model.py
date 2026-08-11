"""
Dataset Generator and Machine Learning Model Trainer for Post-Diagnosis Cancer Survival Prediction.
Generates clinical survival data for patients diagnosed with cancer (4000+ samples).
Trains, evaluates, calibrates, and serializes pipeline to models/survival_pipeline.pkl.
"""

import os
import joblib
import numpy as np
import pandas as pd
from pathlib import Path

from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
    ExtraTreesClassifier,
    HistGradientBoostingClassifier,
)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "dataset" / "cancer_survival_dataset.csv"
MODEL_PATH = BASE_DIR / "models" / "survival_pipeline.pkl"
RANDOM_STATE = 42

NUMERICAL_FEATURES = [
    "age",
    "bmi",
    "tumor_size_cm",
    "diagnosis_months",
]

CATEGORICAL_FEATURES = [
    "gender",
    "smoking_status",
    "hospital_region",
    "has_diabetes",
    "has_hypertension",
    "has_heart_disease",
    "has_kidney_disease",
    "cancer_type",
    "stage",
    "metastasis",
    "lymph_nodes",
    "genetic_marker",
    "treatment_type",
    "treatment_response",
]


def generate_survival_dataset(num_samples: int = 5000) -> pd.DataFrame:
    """Generates synthetic medically calibrated clinical survival data."""
    np.random.seed(RANDOM_STATE)

    age = np.random.randint(20, 85, size=num_samples)
    gender = np.random.choice(["Male", "Female"], size=num_samples, p=[0.48, 0.52])
    bmi = np.round(np.random.normal(25.5, 4.5, size=num_samples), 1)
    bmi = np.clip(bmi, 16.0, 42.0)

    smoking_status = np.random.choice(["Never", "Former", "Current"], size=num_samples, p=[0.55, 0.25, 0.20])
    hospital_region = np.random.choice(["North", "South", "East", "West"], size=num_samples)

    has_diabetes = np.random.choice(["Yes", "No"], size=num_samples, p=[0.20, 0.80])
    has_hypertension = np.random.choice(["Yes", "No"], size=num_samples, p=[0.30, 0.70])
    has_heart_disease = np.random.choice(["Yes", "No"], size=num_samples, p=[0.12, 0.88])
    has_kidney_disease = np.random.choice(["Yes", "No"], size=num_samples, p=[0.08, 0.92])

    cancer_type = np.random.choice(["Breast", "Colon", "Lung", "Prostate", "Leukemia", "Skin", "Other"], size=num_samples)
    stage = np.random.choice(["Stage I", "Stage II", "Stage III", "Stage IV"], size=num_samples, p=[0.30, 0.35, 0.23, 0.12])

    tumor_size_cm = np.round(np.random.uniform(0.5, 12.0, size=num_samples), 1)
    diagnosis_months = np.random.randint(1, 72, size=num_samples)

    metastasis = [
        np.random.choice(["Yes", "No"], p=[0.75, 0.25]) if st == "Stage IV" else (
            np.random.choice(["Yes", "No"], p=[0.35, 0.65]) if st == "Stage III" else "No"
        )
        for st in stage
    ]

    lymph_nodes = [
        np.random.choice(["Yes", "No"], p=[0.80, 0.20]) if st in ["Stage III", "Stage IV"] else np.random.choice(["Yes", "No"], p=[0.25, 0.75])
        for st in stage
    ]

    genetic_marker = np.random.choice(["BRCA1", "BRCA2", "KRAS", "EGFR", "TP53", "None"], size=num_samples, p=[0.10, 0.10, 0.15, 0.15, 0.15, 0.35])

    treatment_type = np.random.choice(["Surgery", "Chemotherapy", "Radiation Therapy", "Immunotherapy", "Targeted Therapy", "Combination Therapy"], size=num_samples)
    treatment_response = np.random.choice(["Excellent", "Good", "Stable", "Partial Response", "No Response", "Disease Progression"], size=num_samples, p=[0.25, 0.30, 0.20, 0.12, 0.08, 0.05])

    # Epidemiological survival scoring model
    score = 80.0

    # Stage impact
    stage_weights = {"Stage I": 25.0, "Stage II": 10.0, "Stage III": -15.0, "Stage IV": -40.0}
    for i, st in enumerate(stage):
        score += stage_weights[st]

    # Treatment response impact
    resp_weights = {
        "Excellent": 30.0,
        "Good": 20.0,
        "Stable": 5.0,
        "Partial Response": -5.0,
        "No Response": -20.0,
        "Disease Progression": -35.0,
    }

    score_arr = np.zeros(num_samples) + 60.0
    for i in range(num_samples):
        s_val = 60.0
        s_val += stage_weights[stage[i]]
        s_val += resp_weights[treatment_response[i]]
        if metastasis[i] == "Yes":
            s_val -= 25.0
        if lymph_nodes[i] == "Yes":
            s_val -= 12.0
        if smoking_status[i] == "Current":
            s_val -= 15.0
        if has_heart_disease[i] == "Yes" or has_kidney_disease[i] == "Yes":
            s_val -= 10.0
        if age[i] > 65:
            s_val -= 12.0
        if tumor_size_cm[i] > 5.0:
            s_val -= (tumor_size_cm[i] - 5.0) * 3.0
        score_arr[i] = s_val

    noise = np.random.normal(0, 8.0, size=num_samples)
    final_score = np.clip(score_arr + noise, 10, 140)
    survival_prob = 1.0 / (1.0 + np.exp(-(final_score - 45.0) / 22.0))
    survival_label = (survival_prob >= 0.50).astype(int)

    df = pd.DataFrame({
        "age": age,
        "gender": gender,
        "bmi": bmi,
        "smoking_status": smoking_status,
        "hospital_region": hospital_region,
        "has_diabetes": has_diabetes,
        "has_hypertension": has_hypertension,
        "has_heart_disease": has_heart_disease,
        "has_kidney_disease": has_kidney_disease,
        "cancer_type": cancer_type,
        "stage": stage,
        "tumor_size_cm": tumor_size_cm,
        "diagnosis_months": diagnosis_months,
        "metastasis": metastasis,
        "lymph_nodes": lymph_nodes,
        "genetic_marker": genetic_marker,
        "treatment_type": treatment_type,
        "treatment_response": treatment_response,
        "survival_label": survival_label,
    })

    DATASET_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATASET_PATH, index=False)
    print(f"Generated survival dataset with {len(df)} samples saved to {DATASET_PATH}")
    return df


def build_preprocessor() -> ColumnTransformer:
    num_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    cat_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])

    return ColumnTransformer(
        transformers=[
            ("num", num_transformer, NUMERICAL_FEATURES),
            ("cat", cat_transformer, CATEGORICAL_FEATURES),
        ]
    )


def train_survival_model():
    print("Initializing survival dataset generation and model training...")
    if not DATASET_PATH.exists():
        df = generate_survival_dataset()
    else:
        df = pd.read_csv(DATASET_PATH)

    X = df.drop(columns=["survival_label"])
    y = df["survival_label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )

    preprocessor = build_preprocessor()

    models = {
        "GradientBoosting": GradientBoostingClassifier(n_estimators=200, learning_rate=0.08, max_depth=5, random_state=RANDOM_STATE),
        "RandomForest": RandomForestClassifier(n_estimators=250, max_depth=12, random_state=RANDOM_STATE),
        "ExtraTrees": ExtraTreesClassifier(n_estimators=250, max_depth=12, random_state=RANDOM_STATE),
        "HistGradientBoosting": HistGradientBoostingClassifier(max_iter=200, learning_rate=0.08, max_depth=6, random_state=RANDOM_STATE),
        "LogisticRegression": LogisticRegression(max_iter=1000, random_state=RANDOM_STATE),
    }

    print("\n--- Evaluating Survival Models with 5-Fold Cross Validation ---")
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    best_name = None
    best_score = 0.0

    for name, clf in models.items():
        pipeline = Pipeline([
            ("preprocessor", preprocessor),
            ("classifier", clf)
        ])
        scores = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="roc_auc", n_jobs=-1)
        mean_auc = np.mean(scores)
        print(f"Model: {name:<22} | 5-Fold CV ROC-AUC: {mean_auc:.4f} (+/- {np.std(scores):.4f})")
        if mean_auc > best_score:
            best_score = mean_auc
            best_name = name

    print(f"\nTop Performing Algorithm for Survival Prediction: {best_name} (ROC-AUC: {best_score:.4f})")

    best_clf = models[best_name]
    final_pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", best_clf)
    ])

    calibrated_clf = CalibratedClassifierCV(estimator=final_pipeline, cv=5)
    calibrated_clf.fit(X_train, y_train)

    y_pred = calibrated_clf.predict(X_test)
    y_proba = calibrated_clf.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_proba)

    print("\n=== Final Test Evaluation Metrics (Survival Prediction) ===")
    print(f"Accuracy:  {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall:    {rec:.4f}")
    print(f"F1 Score:  {f1:.4f}")
    print(f"ROC-AUC:   {auc:.4f}")

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({
        "pipeline": final_pipeline,
        "calibrated": calibrated_clf,
        "numerical_features": NUMERICAL_FEATURES,
        "categorical_features": CATEGORICAL_FEATURES,
        "model_name": best_name,
        "metrics": {"accuracy": acc, "precision": prec, "recall": rec, "f1": f1, "auc": auc}
    }, MODEL_PATH)

    print(f"\nTrained survival model pipeline successfully saved to: {MODEL_PATH}")


if __name__ == "__main__":
    train_survival_model()
