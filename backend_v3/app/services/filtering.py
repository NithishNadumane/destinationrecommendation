import pandas as pd


def filter_places(df, user):

    # -----------------------------
    # Distance Filter
    # -----------------------------
    filtered = df[
        df["distance"] <= user["max_distance"]
    ].copy()

    # Normalize category names
    filtered["category"] = (
        filtered["category"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # -----------------------------
    # No preference selected
    # -----------------------------
    if all(int(p.preference) == 0 for p in user["trip_type"]):
        return filtered

    # -----------------------------
    # Minimum rating for each priority
    # -----------------------------
    min_rating = {
        1: 3.0,
        2: 3.5,
        3: 4.0,
        4: 4.3,
        5: 4.5
    }

    # -----------------------------
    # User Preferences
    # -----------------------------
    preference_map = {
        p.type.strip().lower(): int(p.preference)
        for p in user["trip_type"]
        if int(p.preference) > 0
    }

    # -----------------------------
    # Filter by category + rating
    # -----------------------------
    filtered = filtered[
        filtered.apply(
            lambda row:
                row["category"] in preference_map and
                row["rating"] >= min_rating[preference_map[row["category"]]],
            axis=1
        )
    ]

    return filtered.reset_index(drop=True)