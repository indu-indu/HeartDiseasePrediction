import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

print("Loading real dataset...")
df = pd.read_csv('cardio_train.csv', sep=';', engine='python')

print("Preprocessing real dataset...")
# Clean missing/outliers per the notebook
df = df.dropna()
df = df[df['height'].between(120, 210)]
df = df[df['weight'].between(30, 200)]
df = df[df['ap_hi'].between(80, 250)]
df = df[df['ap_lo'].between(40, 150)]

df['age_years'] = (df['age'] / 365).astype(int)
df['bmi'] = df['weight'] / (df['height'] / 100) ** 2
df['pulse_pressure'] = df['ap_hi'] - df['ap_lo']
df['map'] = (df['ap_hi'] + 2 * df['ap_lo']) / 3

df = pd.get_dummies(df, columns=['cholesterol', 'gluc'], prefix=['chol', 'glu'], drop_first=True)

num_cols = ['age_years', 'height', 'weight', 'bmi', 'ap_hi', 'ap_lo', 'pulse_pressure', 'map']
cat_cols = ['gender', 'smoke', 'alco', 'active', 'chol_2', 'chol_3', 'glu_2', 'glu_3']

for col in cat_cols:
    if col not in df.columns:
        df[col] = 0

feature_cols = num_cols + cat_cols

X = df[feature_cols]
y = df['cardio']

print("Splitting into 80% train and 20% test...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print("Scaling data...")
scaler = StandardScaler()
X_train[num_cols] = scaler.fit_transform(X_train[num_cols])
X_test[num_cols] = scaler.transform(X_test[num_cols])

# Train models
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42),
    "XGBoost": XGBClassifier(eval_metric='logloss', random_state=42)
    # SVM skipped here to save time; it takes exceptionally long to train on 50k rows
}

best_acc = 0
best_model_name = ""
best_model = None

print("\nEvaluating Models on Test Data:")
for name, model in models.items():
    print(f"Training {name}...")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"[{name}] Accuracy: {acc:.4f}")
    
    if acc > best_acc:
        best_acc = acc
        best_model_name = name
        best_model = model

print(f"\nWINNER: {best_model_name} with Accuracy {best_acc:.4f}!")

print(f"Saving {best_model_name} as the final application model...")
os.makedirs("models", exist_ok=True)
joblib.dump(best_model, 'models/model.pkl')
joblib.dump(scaler, 'models/scaler.pkl')
print("Done! The web app will now use the best model.")
