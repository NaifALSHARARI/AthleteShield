# training_app/predictor.py

import os
import pandas as pd
import joblib
from django.conf import settings

MODEL_PATH = os.path.join(settings.BASE_DIR, 'training_app', 'injury_model.pkl')
pipeline_model = joblib.load(MODEL_PATH)

def get_injury_risk(minutes_played, training_load, prev_injuries, age):
    """
    يأخذ بيانات اللاعب ويُرجع احتمالية الإصابة (قيمة بين 0 و 1)
    """
    X = pd.DataFrame([{
        'minutes_played': minutes_played,
        'training_load': training_load,
        'prev_injuries': prev_injuries,
        'age': age
    }])
    prob = pipeline_model.predict_proba(X)[0][1]
    return prob
