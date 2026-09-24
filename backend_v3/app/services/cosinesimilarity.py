from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from app.core.constants import CATEGORY_LIST


def run_similarity(df, user):

    feature_cols = [cat.lower() for cat in CATEGORY_LIST]

    X = df[feature_cols]

    priority_to_weight = {
        1: 1.0,
        2: 0.8,
        3: 0.6,
        4: 0.4,
        5: 0.2
    }

    # Build user vector
    user_vector = []

    has_preference = any(
        int(p.preference) > 0
        for p in user["trip_type"]
    )

    for cat in CATEGORY_LIST:

        if not has_preference:
            # No preferences -> every category equal
            user_vector.append(1.0)
            continue

        weight = 0.0

        for pref in user["trip_type"]:

            if (
                pref.type.strip().lower()
                == cat.lower()
            ):
                weight = priority_to_weight.get(
                    int(pref.preference),
                    0.0
                )
                break

        user_vector.append(weight)

    user_vector = np.array(user_vector).reshape(1, -1)

    similarity = cosine_similarity(
        user_vector,
        X
    )[0]

    df = df.copy()

    df["similarity"] = similarity

    return df.sort_values(
        by="similarity",
        ascending=False
    )