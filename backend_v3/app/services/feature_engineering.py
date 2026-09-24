from app.core.constants import CATEGORY_LIST
from sklearn.preprocessing import MinMaxScaler


def get_category_weights(user):
    """
    Convert user priorities into weights.

    Priority:
        1 -> 1.0
        2 -> 0.8
        3 -> 0.6
        4 -> 0.4
        5 -> 0.2
        0 -> Not Preferred
    """

    priority_to_weight = {
        1: 1.0,
        2: 0.8,
        3: 0.6,
        4: 0.4,
        5: 0.2
    }

    # No preferences selected
    if all(int(p.preference) == 0 for p in user["trip_type"]):
        return {
            cat.lower(): 1.0
            for cat in CATEGORY_LIST
        }

    weights = {
        cat.lower(): 0.0
        for cat in CATEGORY_LIST
    }

    for pref in user["trip_type"]:

        priority = int(pref.preference)

        if priority == 0:
            continue

        weights[pref.type.strip().lower()] = priority_to_weight[priority]

    return weights


def transform_features(df, user):

    df = df.copy()

    # Normalize category names
    df["category"] = (
        df["category"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    weights = get_category_weights(user)

    # One-hot weighted category vectors
    for cat in CATEGORY_LIST:

        cat = cat.lower()

        df[cat] = (
            (df["category"] == cat)
            .astype(float)
            * weights[cat]
        )

    # -----------------------------
    # Fill missing values
    # -----------------------------
    df["rating"] = df["rating"].fillna(
        df["rating"].median()
    )

    df["popularity"] = df["popularity"].fillna(
        df["popularity"].median()
    )

    # -----------------------------
    # Normalize ONLY popularity
    # -----------------------------
    if len(df) > 1:

        scaler = MinMaxScaler()

        df[["popularity"]] = scaler.fit_transform(
            df[["popularity"]]
        )

    else:

        df["popularity"] = 0.5

    return df