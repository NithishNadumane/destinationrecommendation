import pandas as pd
from app.core.config import DATA_PATH


def load_data():
    df = pd.read_csv(DATA_PATH)

    # Rename required columns
    df = df.rename(columns={
        "place_name": "name",
        "latitude": "lat",
        "longitude": "lon"
    })

    # Standardize category names
    df["category"] = df["category"].str.strip().str.title()

    # Normalize popularity (0-1)
    if df["popularity"].max() > 1:
        df["popularity"] = df["popularity"].clip(0, 100) / 100.0

    # Normalize rating (0-1)
    if df["rating"].max() > 1:
        df["rating"] = df["rating"].clip(0, 5) 

    return df