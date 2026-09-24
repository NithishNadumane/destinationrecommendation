import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GCP_API_KEY")
)


def generate_district_information(district, weather):

    try:

        weather = weather or {}

        current = weather.get("current", {})

        temperature = current.get("temperature_2m")
        humidity = current.get("relative_humidity_2m")
        precipitation = current.get("precipitation")
        wind_speed = current.get("wind_speed_10m")

        prompt = f"""
You are a travel assistant.

District: {district}

Temperature: {temperature} °C
Humidity: {humidity} %
Rain: {precipitation} mm
Wind: {wind_speed} km/h

Give ONE short travel statement based on
the current weather.

Do not mention exact weather numbers.
Return only one short sentence.
"""

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        statement = response.text.strip()

        return {
            "temperature": temperature,
            "humidity": humidity,
            "precipitation": precipitation,
            "wind_speed": wind_speed,
            "statement": statement
        }

    except Exception as e:

        print(
            f"Gemini Error for {district}:",
            e
        )

        return {
            "temperature": None,
            "humidity": None,
            "precipitation": None,
            "wind_speed": None,
            "statement": "Weather information is currently unavailable."
        }