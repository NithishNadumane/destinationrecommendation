from app.services.data_loader import load_data
from app.services.preprocessing import process_input
from app.services.distance import add_distance
from app.services.filtering import filter_places
from app.services.feature_engineering import transform_features
from app.services.cosinesimilarity import run_similarity
from app.services.ranking import rank_places

from app.services.image_service import (
    get_place_images,
    find_place_image
)

from app.services.weather_service import (
    get_district_weather
)

from app.services.district_ai_service import (
    generate_district_information
)

import re


# ============================================================
# Slug Generator
# ============================================================

def slugify(text):

    return re.sub(
        r"[^a-z0-9]+",
        "-",
        str(text).lower()
    ).strip("-")


# ============================================================
# District Score
# ============================================================

def calculate_district_score(
    group,
    max_places
):

    avg_score = group["score"].mean()

    place_score = (
        len(group) / max_places
    )

    return (
        0.8 * avg_score +
        0.2 * place_score
    )


# ============================================================
# Main Recommendation
# ============================================================

def recommend_places(user_input):

    try:

        # ====================================================
        # Load Data
        # ====================================================

        print("Loading Data...")

        df = load_data()


        # ====================================================
        # Load Images
        # ====================================================

        print(
            "Loading Images From PostgreSQL..."
        )

        image_data = get_place_images()


        # ====================================================
        # Process User Input
        # ====================================================

        print(
            "Processing User Input..."
        )

        user = process_input(
            user_input
        )


        # ====================================================
        # Calculate Distance
        # ====================================================

        print(
            "Calculating Distance..."
        )

        df = add_distance(
            df,
            user
        )


        # ====================================================
        # Filtering
        # ====================================================

        print(
            "Filtering..."
        )

        df = filter_places(
            df,
            user
        )


        # ====================================================
        # No Results
        # ====================================================

        if df.empty:

            return {
                "results": []
            }


        # ====================================================
        # Feature Engineering
        # ====================================================

        print(
            "Feature Engineering..."
        )

        df = transform_features(
            df,
            user
        )


        # ====================================================
        # Cosine Similarity
        # ====================================================

        print(
            "Cosine Similarity..."
        )

        df = run_similarity(
            df,
            user
        )


        # ====================================================
        # Ranking
        # ====================================================

        print(
            "Ranking Places..."
        )

        df = rank_places(
            df,
            user
        )


        # ====================================================
        # Group By District
        # ====================================================

        groups = df.groupby(
            "district"
        )

        max_places = groups.size().max()

        district_scores = []


        # ====================================================
        # Calculate District Scores
        # ====================================================

        for district, group in groups:

            district_score = (
                calculate_district_score(
                    group,
                    max_places
                )
            )

            district_scores.append(
                (
                    district,
                    district_score
                )
            )


        # ====================================================
        # Sort Districts
        # ====================================================

        district_scores.sort(
            key=lambda x: x[1],
            reverse=True
        )


        results = []


        # ====================================================
        # Top 5 Districts
        # ====================================================

        for district, district_score in district_scores[:5]:

            print(
                f"\nProcessing district: {district}"
            )


            group = groups.get_group(
                district
            )


            # =================================================
            # Highest Score First
            # =================================================

            group = group.sort_values(

                by=[
                    "score",
                    "rating"
                ],

                ascending=[
                    False,
                    False
                ]
            )


            places = []


            # =================================================
            # Add Places
            # =================================================

            for _, row in group.iterrows():

                place = row.to_dict()


                # ---------------------------------------------
                # District Slug
                # ---------------------------------------------

                place["district_slug"] = slugify(
                    place["district"]
                )


                # ---------------------------------------------
                # Place Slug
                # ---------------------------------------------

                place["place_slug"] = slugify(
                    place["name"]
                )


                # =============================================
                # Find Image
                # =============================================

                place["image_url"] = (
                    find_place_image(

                        place_name=place["name"],

                        district_name=place["district"],

                        image_data=image_data,

                        threshold=0.70
                    )
                )


                places.append(
                    place
                )


            # =================================================
            # Get Weather
            # =================================================

            print(
                f"Getting weather for {district}..."
            )

            weather = get_district_weather(
                district
            )


            # =================================================
            # Generate AI Information
            # =================================================

            print(
                f"Generating AI information "
                f"for {district}..."
            )

            district_info = (
                generate_district_information(

                    district=district,

                    weather=weather
                )
            )


            # =================================================
            # Add District Result
            # =================================================

            results.append(

                {

                    "district": district,

                    "district_score": round(
                        district_score,
                        3
                    ),

                    "total_places": len(
                        places
                    ),

                    "district_info": district_info,

                    "places": places
                }

            )


        # ====================================================
        # Final Response
        # ====================================================

        return {

            "results": results

        }


    except Exception as e:

        print(
            "Recommendation Error:",
            e
        )

        return {

            "error": str(e)

        }