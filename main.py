import os
from datetime import datetime
import requests
from dotenv import load_dotenv

# 1. Load environment variables from .env
load_dotenv()
API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")

# 2. Custom class to organize and display the retrieved data (Weather)
class WeatherReport:
    def __init__(self, city, temperature, wind_speed, observation_time):
        self.city = city
        self.temperature = temperature
        self.wind_speed = wind_speed
        self.observation_time = observation_time

    def display_summary(self):
        print("=" * 42)
        print(f"Weather Summary for {self.city}")
        print("=" * 42)
        print(f"Temperature      : {self.temperature} °C")
        print(f"Wind Speed       : {self.wind_speed} km/h")
        print(f"Observation Time : {self.observation_time}")
        print("=" * 42)

# 3. Fetch and parse JSON from the API
def get_weather(city_name, lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": "true",
        "timezone": "Africa/Cairo"
    }
    headers = {"X-Client-Key": API_KEY}

    response = requests.get(API_URL, params=params, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()
    current = data["current_weather"]
    tz_abbr = data.get("timezone_abbreviation", "Local")

    # The API updates weather observations at 15-minute intervals
    parsed_time = datetime.fromisoformat(current["time"])
    formatted_time = parsed_time.strftime(f"%Y-%m-%d %I:%M %p ({tz_abbr})")
    
    return WeatherReport(
        city=city_name,
        temperature=current["temperature"],
        wind_speed=current["windspeed"],
        observation_time=formatted_time
    )

if __name__ == "__main__":
    if not API_URL:
        print("Error: API_URL is missing in the .env file.")
    else:
        report = get_weather("Mansoura", 31.0409, 31.3785)
        report.display_summary()
