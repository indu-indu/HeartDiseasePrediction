import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os

print("Loading dataset...")
df = pd.read_csv('cardio_train.csv', sep=';', engine='python')

print("Preprocessing...")
# Match the exact preprocessing from heart.ipynb
df['age_years'] = (df['age'] / 365).astype(int)
df['bmi'] = df['weight'] / (df['height'] / 100) ** 2
df['pulse_pressure'] = df['ap_hi'] - df['ap_lo']
df['map'] = (df['ap_hi'] + 2 * df['ap_lo']) / 3

# Filter outliers matching the notebook
df = df[df['height'].between(120, 210)]
df = df[df['weight'].between(30, 200)]
df = df[df['ap_hi'].between(80, 250)]
df = df[df['ap_lo'].between(40, 150)]

df = pd.get_dummies(df, columns=['cholesterol', 'gluc'], prefix=['chol', 'glu'], drop_first=True)

num_cols = ['age_years', 'height', 'weight', 'bmi', 'ap_hi', 'ap_lo', 'pulse_pressure', 'map']
cat_cols = ['gender', 'smoke', 'alco', 'active', 'chol_2', 'chol_3', 'glu_2', 'glu_3']

# Handle potentially missing dummy columns if values 2/3 weren't present (highly unlikely for 70k dataset, but safe)
for col in cat_cols:
    if col not in df.columns:
        df[col] = 0

feature_cols = num_cols + cat_cols

print("Scaling data...")
scaler = StandardScaler()
df[num_cols] = scaler.fit_transform(df[num_cols])

X = df[feature_cols]
y = df['cardio']

print("Training Random Forest model on REAL data...")
model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
model.fit(X, y)

os.makedirs("models", exist_ok=True)
joblib.dump(model, 'models/model.pkl')
joblib.dump(scaler, 'models/scaler.pkl')

print("Successfully trained and saved real model.pkl and scaler.pkl!")
