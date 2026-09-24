from app.core.database import get_connection

import re
from difflib import SequenceMatcher


# --------------------------------------------------
# Normalize text
# --------------------------------------------------
def normalize_text(text):
    """
    Convert text to lowercase and remove unnecessary
    spaces and special characters.
    """

    if text is None:
        return ""

    text = str(text).lower().strip()

    # Replace special characters with spaces
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # Remove multiple spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# --------------------------------------------------
# Calculate similarity
# --------------------------------------------------
def similarity(text1, text2):

    text1 = normalize_text(text1)
    text2 = normalize_text(text2)

    if not text1 or not text2:
        return 0

    return SequenceMatcher(
        None,
        text1,
        text2
    ).ratio()


# --------------------------------------------------
# Load all place images
# --------------------------------------------------
def get_place_images():

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                p.name AS place_name,
                d.name AS district_name,
                i.src AS image_url
            FROM places p

            JOIN districts d
                ON p.district_id = d.id

            LEFT JOIN LATERAL (
                SELECT src
                FROM images
                WHERE images.place_id = p.id
                ORDER BY images.id
                LIMIT 1
            ) i ON TRUE
        """)

        rows = cursor.fetchall()

        places = []

        for place_name, district_name, image_url in rows:

            places.append({
                "place_name": place_name,
                "district_name": district_name,
                "image_url": image_url
            })

        return places

    finally:

        cursor.close()
        conn.close()


# --------------------------------------------------
# Find image for a place
# --------------------------------------------------
def find_place_image(
    place_name,
    district_name,
    image_data,
    threshold=0.70
):

    # ----------------------------------------------
    # Normalize district
    # ----------------------------------------------
    target_district = normalize_text(
        district_name
    )

    # ----------------------------------------------
    # Normalize place
    # ----------------------------------------------
    target_place = normalize_text(
        place_name
    )

    if not target_district or not target_place:
        return None


    # ==================================================
    # STEP 1
    # STRICT DISTRICT MATCH
    # ==================================================

    district_matches = []

    for item in image_data:

        database_district = normalize_text(
            item["district_name"]
        )

        # STRICT district comparison
        if database_district == target_district:

            district_matches.append(item)


    # No district match
    if not district_matches:
        return None


    # ==================================================
    # STEP 2
    # EXACT PLACE MATCH
    # ==================================================

    for item in district_matches:

        database_place = normalize_text(
            item["place_name"]
        )

        if database_place == target_place:

            return item["image_url"]


    # ==================================================
    # STEP 3
    # APPROXIMATE PLACE MATCH
    # ==================================================

    best_match = None
    best_score = 0

    for item in district_matches:

        database_place = normalize_text(
            item["place_name"]
        )

        score = similarity(
            target_place,
            database_place
        )

        if score > best_score:

            best_score = score
            best_match = item


    # ==================================================
    # STEP 4
    # THRESHOLD CHECK
    # ==================================================

    if best_match and best_score >= threshold:

        print(
            f"Approx match: "
            f"'{place_name}' → "
            f"'{best_match['place_name']}' "
            f"(score={best_score:.2f})"
        )

        return best_match["image_url"]


    # No sufficiently good match
    print(
        f"No image match for "
        f"'{place_name}' "
        f"in district '{district_name}' "
        f"(best score={best_score:.2f})"
    )

    return None