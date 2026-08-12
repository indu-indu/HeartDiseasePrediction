from ml.predictor import predictor

data = {
    "age": 60,
    "gender": 1,
    "height": 150,
    "weight": 60,
    "ap_hi": 120,
    "ap_lo": 100,
    "cholesterol": 1,
    "gluc": 1,
    "smoke": 0,
    "alco": 0,
    "active": 0
}

print("User Input Prediction:", predictor.predict(data))
