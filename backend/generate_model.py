import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os

# Create synthetic data that mimics the cardiovascular disease dataset
np.random.seed(42)
n_samples = 1000

data = {
    'age': np.random.randint(14000, 23000, n_samples), # days
    'gender': np.random.choice([1, 2], n_samples),
    'height': np.random.normal(165, 10, n_samples),
    'weight': np.random.normal(75, 15, n_samples),
    'ap_hi': np.random.normal(120, 20, n_samples),
    'ap_lo': np.random.normal(80, 15, n_samples),
    'cholesterol': np.random.choice([1, 2, 3], n_samples),
    'gluc': np.random.choice([1, 2, 3], n_samples),
    'smoke': np.random.choice([0, 1], n_samples),
    'alco': np.random.choice([0, 1], n_samples),
    'active': np.random.choice([0, 1], n_samples),
    'cardio': np.random.choice([0, 1], n_samples)
}

df = pd.DataFrame(data)

# Preprocessing to match the notebook
df['age_years'] = (df['age']/365).astype(int)
df['bmi'] = df['weight'] / (df['height'] / 100) ** 2
df['pulse_pressure'] = df['ap_hi'] - df['ap_lo']
df['map'] = (df['ap_hi'] + 2 * df['ap_lo']) / 3

# Dummy encoding
df = pd.get_dummies(df, columns=['cholesterol', 'gluc'], prefix=['chol', 'glu'], drop_first=True)

# Define columns expected by model
num_cols = ['age_years', 'height', 'weight', 'bmi', 'ap_hi', 'ap_lo', 'pulse_pressure', 'map']
cat_cols = ['gender', 'smoke', 'alco', 'active', 'chol_2', 'chol_3', 'glu_2', 'glu_3']
feature_cols = num_cols + cat_cols

# Scale numerical columns
scaler = StandardScaler()
df[num_cols] = scaler.fit_transform(df[num_cols])

X = df[feature_cols]
y = df['cardio']

# Train a model
print("Training dummy RandomForest model...")
model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X, y)

# Ensure models directory exists
os.makedirs("models", exist_ok=True)

# Save model and scaler
joblib.dump(model, 'models/model.pkl')
joblib.dump(scaler, 'models/scaler.pkl')

print("Saved models/model.pkl and models/scaler.pkl successfully.")
