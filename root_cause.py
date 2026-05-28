# root_cause.py
import numpy as np

def analyze_risk(input_data, model, feature_names):
    # Predict risk probabilities
    probs = model.predict_proba([input_data])[0]
    # Get predicted class
    risk_class = model.predict([input_data])[0]
    
    # Feature importance
    importances = model.feature_importances_
    top_features = sorted(
        zip(feature_names, importances), key=lambda x: x[1], reverse=True
    )
    return risk_class, top_features[:30]  
