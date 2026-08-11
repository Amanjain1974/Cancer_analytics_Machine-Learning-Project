"""
Comprehensive Dataset Generator and Machine Learning Model Trainer for Pre-Diagnosis AI Cancer Risk Assessment.
Generates an epidemiological dataset based on NCI, CDC, WHO, and BRFSS cancer risk parameters (40+ features).
Trains, evaluates, calibrates, and serializes the top-performing ML pipeline to models/model_pipeline.pkl.
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
DATASET_PATH = BASE_DIR / "dataset" / "cancer_lifestyle_risk_dataset.csv"
MODEL_PATH = BASE_DIR / "models" / "model_pipeline.pkl"
RANDOM_STATE = 42

NUMERICAL_FEATURES = [
    "age",
    "height_cm",
    "weight_kg",
    "bmi",
    "family_affected_count",
    "cigarettes_per_day",
    "daily_walking_mins",
    "sleep_hours",
    "water_intake_liters",
]

CATEGORICAL_FEATURES = [
    "gender",
    "family_history",
    "family_cancer_type",
    "smoking_status",
    "alcohol_intake",
    "tobacco_chewing",
    "exercise_frequency",
    "stress_level",
    "vegetables_intake",
    "fruits_intake",
    "fast_food_frequency",
    "processed_meat",
    "red_meat",
    "sugary_drinks",
    "junk_food_frequency",
    "diabetes",
    "hypertension",
    "obesity",
    "chronic_inflammation",
    "previous_tumors",
    "genetic_disorders",
    "symptom_cough",
    "symptom_blood_stool",
    "symptom_blood_urine",
    "symptom_chest_pain",
    "symptom_swallowing_difficulty",
    "symptom_fatigue",
    "symptom_weight_loss",
    "symptom_fever",
    "symptom_night_sweats",
    "symptom_skin_lesions",
    "symptom_bleeding",
    "symptom_lump",
    "symptom_chronic_pain",
    "symptom_infections",
    "air_pollution",
    "radiation_exposure",
    "chemical_exposure",
    "asbestos_exposure",
    "occupation_risk",
    "uv_exposure",
]


def generate_epidemiological_dataset(num_samples: int = 6000) -> pd.DataFrame:
    """Generates synthetic medically calibrated pre-diagnosis risk data."""
    np.random.seed(RANDOM_STATE)

    age = np.random.randint(18, 86, size=num_samples)
    gender = np.random.choice(["Male", "Female"], size=num_samples, p=[0.49, 0.51])
    height_cm = np.round(np.random.normal(168, 10, size=num_samples), 1)
    height_cm = np.clip(height_cm, 140, 210)
    weight_kg = np.round(np.random.normal(74, 16, size=num_samples), 1)
    weight_kg = np.clip(weight_kg, 40, 150)
    bmi = np.round(weight_kg / ((height_cm / 100.0) ** 2), 1)

    family_history = np.random.choice(["Yes", "No"], size=num_samples, p=[0.30, 0.70])
    family_cancer_type = [
        np.random.choice(["Breast", "Colon", "Lung", "Prostate", "Skin", "Other"]) if fh == "Yes" else "None"
        for fh in family_history
    ]
    family_affected_count = [
        np.random.choice([1, 2, 3], p=[0.65, 0.25, 0.10]) if fh == "Yes" else 0
        for fh in family_history
    ]

    smoking_status = np.random.choice(["Never", "Former", "Occasionally", "Daily"], size=num_samples, p=[0.50, 0.20, 0.15, 0.15])
    cigarettes_per_day = [
        np.random.randint(10, 35) if sm == "Daily" else (np.random.randint(1, 10) if sm in ["Former", "Occasionally"] else 0)
        for sm in smoking_status
    ]

    alcohol_intake = np.random.choice(["Never", "Occasionally", "Weekly", "Daily"], size=num_samples, p=[0.35, 0.35, 0.20, 0.10])
    tobacco_chewing = np.random.choice(["Yes", "No"], size=num_samples, p=[0.12, 0.88])

    exercise_frequency = np.random.choice(["Sedentary", "1-2 times/week", "3-4 times/week", "Daily"], size=num_samples, p=[0.30, 0.30, 0.25, 0.15])
    daily_walking_mins = np.random.randint(5, 120, size=num_samples)
    sleep_hours = np.random.randint(4, 10, size=num_samples)
    stress_level = np.random.choice(["Low", "Moderate", "High"], size=num_samples, p=[0.30, 0.45, 0.25])
    water_intake_liters = np.round(np.random.uniform(0.8, 4.0, size=num_samples), 1)

    vegetables_intake = np.random.choice(["Low", "Moderate", "High"], size=num_samples, p=[0.30, 0.50, 0.20])
    fruits_intake = np.random.choice(["Low", "Moderate", "High"], size=num_samples, p=[0.35, 0.45, 0.20])
    fast_food_frequency = np.random.choice(["Rarely", "Weekly", "Daily"], size=num_samples, p=[0.40, 0.45, 0.15])
    processed_meat = np.random.choice(["Yes", "No"], size=num_samples, p=[0.45, 0.55])
    red_meat = np.random.choice(["Rarely", "Weekly", "Daily"], size=num_samples, p=[0.30, 0.50, 0.20])
    sugary_drinks = np.random.choice(["Rarely", "Weekly", "Daily"], size=num_samples, p=[0.35, 0.45, 0.20])
    junk_food_frequency = np.random.choice(["Low", "Moderate", "High"], size=num_samples, p=[0.30, 0.50, 0.20])

    diabetes = np.random.choice(["Yes", "No"], size=num_samples, p=[0.15, 0.85])
    hypertension = np.random.choice(["Yes", "No"], size=num_samples, p=[0.25, 0.75])
    obesity = ["Yes" if b >= 30.0 else "No" for b in bmi]
    chronic_inflammation = np.random.choice(["Yes", "No"], size=num_samples, p=[0.18, 0.82])
    previous_tumors = np.random.choice(["Yes", "No"], size=num_samples, p=[0.12, 0.88])
    genetic_disorders = np.random.choice(["Yes", "No"], size=num_samples, p=[0.08, 0.92])

    air_pollution = np.random.choice(["Low", "Moderate", "High"], size=num_samples, p=[0.40, 0.40, 0.20])
    radiation_exposure = np.random.choice(["Low", "Moderate", "High"], size=num_samples, p=[0.70, 0.22, 0.08])
    chemical_exposure = np.random.choice(["Low", "Moderate", "High"], size=num_samples, p=[0.65, 0.25, 0.10])
    asbestos_exposure = np.random.choice(["Low", "Moderate", "High"], size=num_samples, p=[0.80, 0.15, 0.05])
    occupation_risk = np.random.choice(["Low", "Moderate", "High"], size=num_samples, p=[0.60, 0.28, 0.12])
    uv_exposure = np.random.choice(["Low", "Moderate", "High"], size=num_samples, p=[0.45, 0.38, 0.17])

    # Epidemiological risk scoring math to determine medical ground truth label
    risk_scores = np.zeros(num_samples)

    risk_scores += (age / 80.0) * 25.0
    risk_scores += np.where(bmi >= 30.0, 18.0, np.where(bmi >= 25.0, 8.0, 0.0))
    risk_scores += np.where(smoking_status == "Daily", 35.0, np.where(smoking_status == "Occasionally", 20.0, np.where(smoking_status == "Former", 12.0, 0.0)))
    risk_scores += (np.array(cigarettes_per_day) / 30.0) * 15.0
    risk_scores += np.where(alcohol_intake == "Daily", 18.0, np.where(alcohol_intake == "Weekly", 8.0, 0.0))
    risk_scores += np.where(tobacco_chewing == "Yes", 16.0, 0.0)
    risk_scores += np.where(family_history == "Yes", 25.0, 0.0) + (np.array(family_affected_count) * 6.0)

    risk_scores += np.where(radiation_exposure == "High", 24.0, np.where(radiation_exposure == "Moderate", 10.0, 0.0))
    risk_scores += np.where(chemical_exposure == "High", 20.0, np.where(chemical_exposure == "Moderate", 8.0, 0.0))
    risk_scores += np.where(asbestos_exposure == "High", 22.0, 0.0)
    risk_scores += np.where(uv_exposure == "High", 15.0, 0.0)

    risk_scores += np.where(previous_tumors == "Yes", 20.0, 0.0)
    risk_scores += np.where(chronic_inflammation == "Yes", 14.0, 0.0)
    risk_scores += np.where(genetic_disorders == "Yes", 18.0, 0.0)

    # Calculate symptom probabilities based on underlying risk score
    symptom_cough = [np.random.choice(["Yes", "No"], p=[min(0.85, 0.05 + rs * 0.006), 1 - min(0.85, 0.05 + rs * 0.006)]) for rs in risk_scores]
    symptom_blood_stool = [np.random.choice(["Yes", "No"], p=[min(0.70, 0.02 + rs * 0.004), 1 - min(0.70, 0.02 + rs * 0.004)]) for rs in risk_scores]
    symptom_blood_urine = [np.random.choice(["Yes", "No"], p=[min(0.70, 0.02 + rs * 0.004), 1 - min(0.70, 0.02 + rs * 0.004)]) for rs in risk_scores]
    symptom_chest_pain = [np.random.choice(["Yes", "No"], p=[min(0.75, 0.04 + rs * 0.005), 1 - min(0.75, 0.04 + rs * 0.005)]) for rs in risk_scores]
    symptom_swallowing_difficulty = [np.random.choice(["Yes", "No"], p=[min(0.65, 0.02 + rs * 0.004), 1 - min(0.65, 0.02 + rs * 0.004)]) for rs in risk_scores]
    symptom_fatigue = [np.random.choice(["Yes", "No"], p=[min(0.90, 0.10 + rs * 0.007), 1 - min(0.90, 0.10 + rs * 0.007)]) for rs in risk_scores]
    symptom_weight_loss = [np.random.choice(["Yes", "No"], p=[min(0.80, 0.03 + rs * 0.006), 1 - min(0.80, 0.03 + rs * 0.006)]) for rs in risk_scores]
    symptom_fever = [np.random.choice(["Yes", "No"], p=[min(0.60, 0.05 + rs * 0.003), 1 - min(0.60, 0.05 + rs * 0.003)]) for rs in risk_scores]
    symptom_night_sweats = [np.random.choice(["Yes", "No"], p=[min(0.65, 0.03 + rs * 0.004), 1 - min(0.65, 0.03 + rs * 0.004)]) for rs in risk_scores]
    symptom_skin_lesions = [np.random.choice(["Yes", "No"], p=[min(0.70, 0.04 + rs * 0.005), 1 - min(0.70, 0.04 + rs * 0.005)]) for rs in risk_scores]
    symptom_bleeding = [np.random.choice(["Yes", "No"], p=[min(0.70, 0.02 + rs * 0.005), 1 - min(0.70, 0.02 + rs * 0.005)]) for rs in risk_scores]
    symptom_lump = [np.random.choice(["Yes", "No"], p=[min(0.80, 0.03 + rs * 0.006), 1 - min(0.80, 0.03 + rs * 0.006)]) for rs in risk_scores]
    symptom_chronic_pain = [np.random.choice(["Yes", "No"], p=[min(0.75, 0.05 + rs * 0.005), 1 - min(0.75, 0.05 + rs * 0.005)]) for rs in risk_scores]
    symptom_infections = [np.random.choice(["Yes", "No"], p=[min(0.65, 0.05 + rs * 0.004), 1 - min(0.65, 0.05 + rs * 0.004)]) for rs in risk_scores]

    # Add symptom impact to risk score
    symptoms_list = [
        symptom_cough, symptom_blood_stool, symptom_blood_urine, symptom_chest_pain,
        symptom_swallowing_difficulty, symptom_fatigue, symptom_weight_loss, symptom_fever,
        symptom_night_sweats, symptom_skin_lesions, symptom_bleeding, symptom_lump,
        symptom_chronic_pain, symptom_infections
    ]
    for s_arr in symptoms_list:
        risk_scores += np.where(np.array(s_arr) == "Yes", 6.0, 0.0)

    # Protective factors
    risk_scores -= np.where(exercise_frequency == "Daily", 12.0, np.where(exercise_frequency == "3-4 times/week", 7.0, 0.0))
    risk_scores -= (daily_walking_mins / 120.0) * 8.0
    risk_scores -= np.where(vegetables_intake == "High", 8.0, 0.0)
    risk_scores -= np.where(fruits_intake == "High", 6.0, 0.0)

    # Normalize probability & add slight noise
    noise = np.random.normal(0, 8.0, size=num_samples)
    final_score = np.clip(risk_scores + noise, 10, 160)
    cancer_risk_prob = 1.0 / (1.0 + np.exp(-(final_score - 65.0) / 24.0))
    cancer_risk_label = (cancer_risk_prob >= 0.45).astype(int)

    df = pd.DataFrame({
        "age": age,
        "gender": gender,
        "height_cm": height_cm,
        "weight_kg": weight_kg,
        "bmi": bmi,
        "family_history": family_history,
        "family_cancer_type": family_cancer_type,
        "family_affected_count": family_affected_count,
        "smoking_status": smoking_status,
        "cigarettes_per_day": cigarettes_per_day,
        "alcohol_intake": alcohol_intake,
        "tobacco_chewing": tobacco_chewing,
        "exercise_frequency": exercise_frequency,
        "daily_walking_mins": daily_walking_mins,
        "sleep_hours": sleep_hours,
        "stress_level": stress_level,
        "water_intake_liters": water_intake_liters,
        "vegetables_intake": vegetables_intake,
        "fruits_intake": fruits_intake,
        "fast_food_frequency": fast_food_frequency,
        "processed_meat": processed_meat,
        "red_meat": red_meat,
        "sugary_drinks": sugary_drinks,
        "junk_food_frequency": junk_food_frequency,
        "diabetes": diabetes,
        "hypertension": hypertension,
        "obesity": obesity,
        "chronic_inflammation": chronic_inflammation,
        "previous_tumors": previous_tumors,
        "genetic_disorders": genetic_disorders,
        "symptom_cough": symptom_cough,
        "symptom_blood_stool": symptom_blood_stool,
        "symptom_blood_urine": symptom_blood_urine,
        "symptom_chest_pain": symptom_chest_pain,
        "symptom_swallowing_difficulty": symptom_swallowing_difficulty,
        "symptom_fatigue": symptom_fatigue,
        "symptom_weight_loss": symptom_weight_loss,
        "symptom_fever": symptom_fever,
        "symptom_night_sweats": symptom_night_sweats,
        "symptom_skin_lesions": symptom_skin_lesions,
        "symptom_bleeding": symptom_bleeding,
        "symptom_lump": symptom_lump,
        "symptom_chronic_pain": symptom_chronic_pain,
        "symptom_infections": symptom_infections,
        "air_pollution": air_pollution,
        "radiation_exposure": radiation_exposure,
        "chemical_exposure": chemical_exposure,
        "asbestos_exposure": asbestos_exposure,
        "occupation_risk": occupation_risk,
        "uv_exposure": uv_exposure,
        "cancer_risk": cancer_risk_label
    })

    DATASET_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATASET_PATH, index=False)
    print(f"Generated dataset with {len(df)} samples saved to {DATASET_PATH}")
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

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", num_transformer, NUMERICAL_FEATURES),
            ("cat", cat_transformer, CATEGORICAL_FEATURES),
        ]
    )
    return preprocessor


def train_and_evaluate():
    print("Initializing dataset generation and model training...")
    if not DATASET_PATH.exists():
        df = generate_epidemiological_dataset()
    else:
        df = pd.read_csv(DATASET_PATH)

    X = df.drop(columns=["cancer_risk"])
    y = df["cancer_risk"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )

    preprocessor = build_preprocessor()

    models = {
        "RandomForest": RandomForestClassifier(n_estimators=250, max_depth=12, random_state=RANDOM_STATE),
        "GradientBoosting": GradientBoostingClassifier(n_estimators=200, learning_rate=0.08, max_depth=5, random_state=RANDOM_STATE),
        "ExtraTrees": ExtraTreesClassifier(n_estimators=250, max_depth=12, random_state=RANDOM_STATE),
        "HistGradientBoosting": HistGradientBoostingClassifier(max_iter=200, learning_rate=0.08, max_depth=6, random_state=RANDOM_STATE),
        "LogisticRegression": LogisticRegression(max_iter=1000, random_state=RANDOM_STATE),
    }

    print("\n--- Evaluating Models with 5-Fold Cross Validation ---")
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

    print(f"\nTop Performing Algorithm: {best_name} (ROC-AUC: {best_score:.4f})")

    # Fit best model and apply Probability Calibration
    best_clf = models[best_name]
    final_pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", best_clf)
    ])

    # Calibrate probability predictions using 5-fold cross validation
    calibrated_clf = CalibratedClassifierCV(estimator=final_pipeline, cv=5)
    calibrated_clf.fit(X_train, y_train)

    # Evaluate test metrics
    y_pred = calibrated_clf.predict(X_test)
    y_proba = calibrated_clf.predict_proba(X_test)[:, 1]


    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_proba)

    print("\n=== Final Test Evaluation Metrics ===")
    print(f"Accuracy:  {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall:    {rec:.4f}")
    print(f"F1 Score:  {f1:.4f}")
    print(f"ROC-AUC:   {auc:.4f}")

    # Save model pipeline
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({
        "pipeline": final_pipeline,
        "calibrated": calibrated_clf,
        "numerical_features": NUMERICAL_FEATURES,
        "categorical_features": CATEGORICAL_FEATURES,
        "model_name": best_name,
        "metrics": {"accuracy": acc, "precision": prec, "recall": rec, "f1": f1, "auc": auc}
    }, MODEL_PATH)

    print(f"\nTrained model pipeline successfully saved to: {MODEL_PATH}")


if __name__ == "__main__":
    train_and_evaluate()
