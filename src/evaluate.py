import os
import json
import pickle
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

test_df = pd.read_csv("data/prepared/test.csv")

y_test = (test_df["IMDB_Rating"] >= 7.8).astype(int)

X_test = test_df.copy()

if "Runtime" in X_test.columns:
    X_test["Runtime"] = X_test["Runtime"].astype(str).str.extract(r'(\d+)').astype(float)

if "Gross" in X_test.columns:
    X_test["Gross"] = X_test["Gross"].astype(str).str.replace(',', '').str.replace(' ', '')
    X_test["Gross"] = pd.to_numeric(X_test["Gross"], errors='coerce')

if "Released_Year" in X_test.columns:
    X_test["Released_Year"] = pd.to_numeric(X_test["Released_Year"], errors='coerce')

cols_to_drop = ['IMDB_Rating', 'Title', 'Overview', 'Director', 'Stars']
X_test = X_test.drop(columns=[c for c in cols_to_drop if c in X_test.columns])

num_cols = X_test.select_dtypes(include=['float64', 'int64']).columns
X_test[num_cols] = X_test[num_cols].fillna(X_test[num_cols].median())

X_test = pd.get_dummies(X_test)

with open("models/model_columns.pkl", "rb") as f:
    model_columns = pickle.load(f)

X_test = X_test.reindex(columns=model_columns, fill_value=0)

with open("models/model.pkl", "rb") as f:
    model = pickle.load(f)

predictions = model.predict(X_test)

metrics = {
    "accuracy": round(float(accuracy_score(y_test, predictions)), 4),
    "precision": round(float(precision_score(y_test, predictions, zero_division=0)), 4),
    "recall": round(float(recall_score(y_test, predictions, zero_division=0)), 4),
    "f1_score": round(float(f1_score(y_test, predictions, zero_division=0)), 4)
}

with open("metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

print(f"Evaluacija završena. Postignuta tačnost (Accuracy): {metrics['accuracy']}")