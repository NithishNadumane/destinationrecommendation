# ============================================================
# Generate District Weather Information
# ============================================================

def generate_district_information(district, weather):

    try:

        weather = weather or {}

        current = weather.get("current", {})

        temperature = current.get("temperature_2m")
        humidity = current.get("relative_humidity_2m")
        precipitation = current.get("precipitation")
        wind_speed = current.get("wind_speed_10m")

        # ----------------------------------------------------
        # Generate Travel Statement
        # ----------------------------------------------------

        if precipitation is not None and precipitation > 5:

            statement = (
                "Rainy conditions may affect outdoor travel today."
            )

        elif wind_speed is not None and wind_speed > 30:

            statement = (
                "Strong winds may affect outdoor activities today."
            )

        elif temperature is not None and temperature > 35:

            statement = (
                "Hot conditions may make outdoor activities uncomfortable."
            )

        elif temperature is not None and temperature < 15:

            statement = (
                "Cool weather is expected, so carry suitable clothing."
            )

        else:

            statement = (
                "The weather looks suitable for outdoor travel today."
            )

        # ----------------------------------------------------
        # Return Weather Information
        # ----------------------------------------------------

        return {
            "temperature": temperature,
            "humidity": humidity,
            "precipitation": precipitation,
            "wind_speed": wind_speed,
            "statement": statement
        }

    except Exception as e:

        print(
            f"Weather Error for {district}:",
            e
        )

        return {
            "temperature": None,
            "humidity": None,
            "precipitation": None,
            "wind_speed": None,
            "statement": "Weather information is currently unavailable."
        }