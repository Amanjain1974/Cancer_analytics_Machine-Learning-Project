import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from .config import DATASET_PATH
from .preprocess import preprocess
from .utils import save_model

def train():
    df = preprocess(pd.read_csv(DATASET_PATH))
    X = df.drop(columns=["Recurrence"])
    y = df["Recurrence"]

    num_cols = X.select_dtypes(include=["number"]).columns
    cat_cols = X.select_dtypes(exclude=["number"]).columns

    pre = ColumnTransformer([
        ("num", SimpleImputer(strategy="median"), num_cols),
        ("cat", Pipeline([
            ("imp", SimpleImputer(strategy="most_frequent")),
            ("ohe", OneHotEncoder(handle_unknown="ignore"))
        ]), cat_cols)
    ])

    model = Pipeline([
        ("preprocessor", pre),
        ("classifier", RandomForestClassifier(n_estimators=200, random_state=42))
    ])

    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)
    model.fit(X_train,y_train)
    save_model(model)
    print("Model trained successfully.")

if __name__=="__main__":
    train()
