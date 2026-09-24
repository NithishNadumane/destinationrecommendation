import numpy as np


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km

    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)

    a = (
        np.sin(dlat / 2) ** 2 +
        np.cos(np.radians(lat1)) *
        np.cos(np.radians(lat2)) *
        np.sin(dlon / 2) ** 2
    )

    return R * 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))


def add_distance(df, user):
    # ✅ safety check
    if user["lat"] is None or user["lon"] is None:
        raise ValueError("Invalid user location")

    # ✅ handle missing data safely
    df = df.dropna(subset=["lat", "lon"]).copy()

    # ✅ ensure numeric types
    df["lat"] = df["lat"].astype(float)
    df["lon"] = df["lon"].astype(float)

    # ✅ calculate distance
    df["distance"] = haversine(
        user["lat"],
        user["lon"],
        df["lat"],
        df["lon"]
    )

    # ✅ ensure positive values
    df["distance"] = df["distance"].clip(lower=0)

    return df