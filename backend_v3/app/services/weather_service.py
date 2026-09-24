import requests


# ============================================================
# Get Weather For District
# ============================================================

def get_district_weather(district):

    try:

        print(f"Getting weather for {district}...")

        # ----------------------------------------------------
        # Find district coordinates
        # ----------------------------------------------------

        geo_url = (
            "https://geocoding-api.open-meteo.com/v1/search"
        )

        geo_params = {
            "name": district,
            "count": 1,
            "language": "en",
            "format": "json"
        }

        geo_response = requests.get(
            geo_url,
            params=geo_params,
            timeout=10
        )

        geo_response.raise_for_status()

        geo_data = geo_response.json()

        if not geo_data.get("results"):

            print(
                f"Coordinates not found for {district}"
            )

            return None

        location = geo_data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]


        # ----------------------------------------------------
        # Get Weather
        # ----------------------------------------------------

        weather_url = (
            "https://api.open-meteo.com/v1/forecast"
        )

        weather_params = {

            "latitude": latitude,

            "longitude": longitude,

            "current": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "apparent_temperature,"
                "precipitation,"
                "weather_code,"
                "wind_speed_10m"
            ),

            "daily": (
                "weather_code,"
                "temperature_2m_max,"
                "temperature_2m_min,"
                "precipitation_probability_max,"
                "sunrise,"
                "sunset"
            ),

            "forecast_days": 5,

            "timezone": "auto"
        }

        response = requests.get(
            weather_url,
            params=weather_params,
            timeout=10
        )

        response.raise_for_status()

        return response.json()


    except Exception as e:

        print(
            f"Weather Error for {district}:",
            e
        )

        return None