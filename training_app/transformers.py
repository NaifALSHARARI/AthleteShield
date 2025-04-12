
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class CustomThresholdsTransformer(BaseEstimator, TransformerMixin):

    def __init__(self, load_threshold=60, age_threshold=35):
        self.load_threshold = load_threshold
        self.age_threshold = age_threshold

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X, columns=['minutes_played','training_load','prev_injuries','age'])

        X_ = X.copy()

        bins = [0, 60, 120, 180, 240, 300, 999999]  
        labels = [1, 2, 3, 4, 5, 6]
        X_['minutes_bin'] = pd.cut(X_['minutes_played'], bins=bins, labels=labels).astype(int)

        X_['high_load_flag'] = (X_['training_load'] > self.load_threshold).astype(int)

        X_['senior_age_flag'] = (X_['age'] > self.age_threshold).astype(int)

        return X_
