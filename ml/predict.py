from .utils import load_model

def predict(features):
    model = load_model()
    pred = model.predict(features)
    prob = model.predict_proba(features) if hasattr(model,"predict_proba") else None
    return pred, prob
