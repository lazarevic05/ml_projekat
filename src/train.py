import os
import pandas as pd
import yaml
import pickle
from sklearn.ensemble import RandomForestClassifier

with open("params.yaml", "r") as f:
    params = yaml.safe_load(f)["train"]

train_df = pd.read_csv("data/prepared/train.csv")

y_train = (train_df["IMDB_Rating"] >= 7.8).astype(int)

X_train = train_df.copy()

if "Runtime" in X_train.columns:
    X_train["Runtime"] = X_train["Runtime"].astype(str).str.extract(r'(\d+)').astype(float)

if "Gross" in X_train.columns:
    X_train["Gross"] = X_train["Gross"].astype(str).str.replace(',', '').str.replace(' ', '')
    X_train["Gross"] = pd.to_numeric(X_train["Gross"], errors='coerce')

if "Released_Year" in X_train.columns:
    X_train["Released_Year"] = pd.to_numeric(X_train["Released_Year"], errors='coerce')

cols_to_drop = ['IMDB_Rating', 'Title', 'Overview', 'Director', 'Stars']
X_train = X_train.drop(columns=[c for c in cols_to_drop if c in X_train.columns])

num_cols = X_train.select_dtypes(include=['float64', 'int64']).columns
X_train[num_cols] = X_train[num_cols].fillna(X_train[num_cols].median())

X_train = pd.get_dummies(X_train)

os.makedirs("models", exist_ok=True)
with open("models/model_columns.pkl", "wb") as f:
    pickle.dump(X_train.columns.tolist(), f)

print("Treniram Random Forest model nad IMDb podacima...")
model = RandomForestClassifier(
    n_estimators=params["n_estimators"],
    max_depth=params["max_depth"],
    random_state=params["random_state"]
)
model.fit(X_train, y_train)

model_path = "models/model.pkl"
with open(model_path, "wb") as f:
    pickle.dump(model, f)

print(f"Model uspešno sačuvan na: {model_path}")