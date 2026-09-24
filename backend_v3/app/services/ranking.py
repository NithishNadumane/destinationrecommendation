def compute_score(row, user):

    rating_score = row["rating"] / 5.0
   
    return (
        0.80 * row["similarity"] +
        0.20 * rating_score
      
    )


def rank_places(df, user):
    df["score"] = df.apply(
        lambda r: compute_score(r, user),
        axis=1
    )

    return df.sort_values(
        by="score",
        ascending=False
    )   