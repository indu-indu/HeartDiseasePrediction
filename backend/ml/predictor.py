import os
import numpy as np
import pandas as pd
import joblib

class HeartDiseasePredictor:
    def __init__(self, model_path: str = "models/model.pkl", scaler_path: str = "models/scaler.pkl"):
        self.model_path = model_path
        self.scaler_path = scaler_path
        self.model = None
        self.scaler = None
        self._load_model()

    def _load_model(self):
        if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
            try:
                self.model = joblib.load(self.model_path)
                self.scaler = joblib.load(self.scaler_path)
                print(f"Model and scaler loaded successfully.")
            except Exception as e:
                print(f"Error loading model: {e}")
        else:
            print(f"Warning: Model or scaler not found. Prediction will return mock data.")

    def preprocess(self, data: dict) -> pd.DataFrame:
        # Expected input features:
        # age (years), gender, height, weight, ap_hi, ap_lo, cholesterol, gluc, smoke, alco, active
        
        # 1. Age 
        age_years = data['age']
        
        # 2. Derived features
        height_m = data['height'] / 100
        bmi = data['weight'] / (height_m ** 2)
        pulse_pressure = data['ap_hi'] - data['ap_lo']
        map_pressure = (data['ap_hi'] + 2 * data['ap_lo']) / 3
        
        # 3. Dummy encoding for cholesterol and gluc
        chol_2 = 1 if data['cholesterol'] == 2 else 0
        chol_3 = 1 if data['cholesterol'] == 3 else 0
        glu_2 = 1 if data['gluc'] == 2 else 0
        glu_3 = 1 if data['gluc'] == 3 else 0

        # Construct dataframe matching exact training columns
        num_cols = ['age_years', 'height', 'weight', 'bmi', 'ap_hi', 'ap_lo', 'pulse_pressure', 'map']
        cat_cols = ['gender', 'smoke', 'alco', 'active', 'chol_2', 'chol_3', 'glu_2', 'glu_3']
        
        row = {
            'age_years': age_years,
            'height': data['height'],
            'weight': data['weight'],
            'bmi': bmi,
            'ap_hi': data['ap_hi'],
            'ap_lo': data['ap_lo'],
            'pulse_pressure': pulse_pressure,
            'map': map_pressure,
            'gender': data['gender'],
            'smoke': data['smoke'],
            'alco': data['alco'],
            'active': data['active'],
            'chol_2': chol_2,
            'chol_3': chol_3,
            'glu_2': glu_2,
            'glu_3': glu_3
        }
        
        df = pd.DataFrame([row])
        
        # 4. Scale numerical columns
        if self.scaler:
            df[num_cols] = self.scaler.transform(df[num_cols])
            
        return df

    def predict(self, data: dict) -> dict:
        if self.model is None or self.scaler is None:
            return {
                "prediction": 1,
                "confidence": 0.65,
                "message": "Model not loaded. This is a mock response."
            }

        try:
            features_df = self.preprocess(data)
            
            # predict_proba returns array like [[prob_class_0, prob_class_1]]
            probs = self.model.predict_proba(features_df)[0]
            prediction_prob = probs[1]
            
            prediction = 1 if prediction_prob >= 0.5 else 0
            confidence = float(prediction_prob) if prediction == 1 else 1.0 - float(prediction_prob)
            
            return {
                "prediction": prediction,
                "confidence": confidence,
                "message": "Success (Using the Optimized Cardiovascular Model)"
            }
        except Exception as e:
            return {
                "prediction": -1,
                "confidence": 0.0,
                "error": str(e)
            }

predictor = HeartDiseasePredictor()
