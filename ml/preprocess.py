import pandas as pd

def preprocess(df):
    df = df.copy()
    if "PatientID" in df.columns:
        df = df.drop(columns=["PatientID"])
    if "GeneticMarker" in df.columns:
        df["GeneticMarker"] = df["GeneticMarker"].fillna("Unknown")
    return df
