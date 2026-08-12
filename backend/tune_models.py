import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

print("Loading real dataset...")
df = pd.read_csv('cardio_train.csv', sep=';', engine='python')

print("Preprocessing real dataset...")
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

# Parameter distributions for RandomizedSearchCV
rf_param_dist = {
    'n_estimators': [100, 200, 300, 500],
    'max_depth': [10, 15, 20, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'bootstrap': [True, False]
}

xgb_param_dist = {
    'n_estimators': [100, 200, 300],
    'max_depth': [3, 5, 7, 10],
    'learning_rate': [0.01, 0.05, 0.1, 0.2],
    'subsample': [0.6, 0.8, 1.0],
    'colsample_bytree': [0.6, 0.8, 1.0]
}

print("\n--- Tuning Random Forest ---")
rf = RandomForestClassifier(random_state=42)
rf_random = RandomizedSearchCV(estimator=rf, param_distributions=rf_param_dist, 
                               n_iter=10, cv=3, verbose=2, random_state=42, n_jobs=-1)
rf_random.fit(X_train, y_train)
best_rf = rf_random.best_estimator_
rf_acc = accuracy_score(y_test, best_rf.predict(X_test))
print(f"Best Random Forest Params: {rf_random.best_params_}")
print(f"Tuned Random Forest Accuracy: {rf_acc:.4f}")

print("\n--- Tuning XGBoost ---")
xgb = XGBClassifier(eval_metric='logloss', random_state=42)
xgb_random = RandomizedSearchCV(estimator=xgb, param_distributions=xgb_param_dist, 
                                n_iter=10, cv=3, verbose=2, random_state=42, n_jobs=-1)
xgb_random.fit(X_train, y_train)
best_xgb = xgb_random.best_estimator_
xgb_acc = accuracy_score(y_test, best_xgb.predict(X_test))
print(f"Best XGBoost Params: {xgb_random.best_params_}")
print(f"Tuned XGBoost Accuracy: {xgb_acc:.4f}")

# Compare and save the ultimate winner
if xgb_acc > rf_acc:
    print(f"\nWINNER: Tuned XGBoost with Accuracy {xgb_acc:.4f}!")
    final_model = best_xgb
else:
    print(f"\nWINNER: Tuned Random Forest with Accuracy {rf_acc:.4f}!")
    final_model = best_rf

os.makedirs("models", exist_ok=True)
joblib.dump(final_model, 'models/model.pkl')
joblib.dump(scaler, 'models/scaler.pkl')
print("Saved the optimal tuned model successfully!")
