import requests


def get_lat_lon(city):
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json"

        res = requests.get(
            url,
            headers={"User-Agent": "travel-app"},
            timeout=5
        ).json()

        if res:
            return float(res[0]["lat"]), float(res[0]["lon"])

    except Exception as e:
        print("Geocoding error:", e)

    return None, None


def process_input(user):
    lat, lon = get_lat_lon(user.location)

    # Fallback to Bangalore if location not found
    if lat is None or lon is None:
        print("Using default location (Bangalore)")
        lat, lon = 12.9716, 77.5946

    return {
        "lat": lat,
        "lon": lon,
        "max_distance": user.max_distance,
        "trip_type": user.trip_type
    }