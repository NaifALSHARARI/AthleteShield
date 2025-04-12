

import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline
from .transformers import CustomThresholdsTransformer

BASE_DIR = os.path.dirname(__file__)

def train_injury_model(
    csv_path=os.path.join(BASE_DIR, 'player_data_extended_v2.csv'),
    model_path=os.path.join(BASE_DIR, 'injury_model.pkl')
):

   
    df = pd.read_csv(csv_path)
    X = df[['minutes_played', 'training_load', 'prev_injuries', 'age']]
    y = df['injury_risk']

    
    pipeline = Pipeline([
        ('threshold_transformer', CustomThresholdsTransformer(
            load_threshold=60, 
            age_threshold=35    
        )),
        ('scaler', StandardScaler()),
        ('smote', SMOTE(random_state=42)),
        ('clf', LogisticRegression(solver='liblinear', penalty='l2', C=0.7, random_state=42))
    ])

    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(pipeline, X, y, cv=skf, scoring='accuracy')
    print("Cross-Validation scores:", cv_scores)
    print("Mean CV accuracy: {:.2f}%".format(cv_scores.mean()*100))

  
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    
    pipeline.fit(X_train, y_train)
    test_accuracy = pipeline.score(X_test, y_test)
    print(f"Final Test accuracy: {test_accuracy*100:.2f}%")

   
    joblib.dump(pipeline, model_path)
    print(f"Model saved to: {model_path}")

if __name__ == '__main__':
   
    train_injury_model()
