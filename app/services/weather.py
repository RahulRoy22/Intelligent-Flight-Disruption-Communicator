import requests
from typing import Optional, Dict

# The base endpoint for the Aviation Weather JSON API
WEATHER_URL = "https://aviationweather.gov/api/data/metar"

def get_current_weather(station_id: str) -> Optional[Dict]:
    """
    Fetches the latest METAR weather report for a specific airport (station_id).
    """
    params = {
        "ids": station_id,
        "format": "json"
    }
    
    try:
        response = requests.get(WEATHER_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # If the airport code is invalid or has no data, the API returns an empty list
        if not data:
            return None
            
        # The API returns a list of recent reports, we just want the latest one (index 0)
        latest_report = data[0]
        
        return {
            "station_id": latest_report.get("icaoId"),
            "observation_time": latest_report.get("obsTime"),
            "raw_metar": latest_report.get("rawOb"), # This is the cryptic string the AI will read!
            "temp_c": latest_report.get("temp"),
            "wind_dir_degrees": latest_report.get("wdir"),
            "wind_speed_knots": latest_report.get("wspd")
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None