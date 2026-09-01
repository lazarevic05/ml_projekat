import os
import pandas as pd
from sqlalchemy import create_engine

DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost") 
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "mldb")

CSV_PATH = "data/dataset.csv" 
TABLE_NAME = "raw_data"

def load_csv_to_postgres():
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"Fajl na putanji '{CSV_PATH}' nije pronađen! Proveri gde se nalazi CSV.")

    print(f"Učitavam CSV fajl: {CSV_PATH}...")
    df = pd.read_csv(CSV_PATH)

    db_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(db_url)

    print(f"Upisujem {len(df)} redova u PostgreSQL tabelu '{TABLE_NAME}'...")
    df.to_sql(TABLE_NAME, engine, if_exists="replace", index=False)
    print("Podaci uspešno prebačeni u PostgreSQL bazu!")

if __name__ == "__main__":
    load_csv_to_postgres()
