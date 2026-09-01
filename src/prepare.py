import os
import pandas as pd
import yaml
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split

with open("params.yaml", "r") as f:
    params = yaml.safe_load(f)["prepare"]

DB_URL = "postgresql://postgres:postgres@localhost:5432/mldb"
engine = create_engine(DB_URL)

print("Čitam podatke iz PostgreSQL baze...")
df = pd.read_sql("SELECT * FROM raw_data", engine)

train_df, test_df = train_test_split(
    df,
    test_size=params["split_ratio"],
    random_state=params["random_state"]
)

os.makedirs("data/prepared", exist_ok=True)
train_df.to_csv("data/prepared/train.csv", index=False)
test_df.to_csv("data/prepared/test.csv", index=False)

print(f"Podaci uspešno podeljeni: {len(train_df)} train, {len(test_df)} test.")