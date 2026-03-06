import requests
from typing import Optional, List, Dict

# The base endpoint for live state vectors
OPENSKY_URL = "https://opensky-network.org/api/states/all"

def get_live_flights(lamin: float, lamax: float, lomin: float, lomax: float) -> Optional[List[Dict]]:
    """
    Fetches live flight data within a specific geographic bounding box.
    """
    params = {
        "lamin": lamin,
        "lamax": lamax,
        "lomin": lomin,
        "lomax": lomax
    }
    
    try:
        # A 10-second timeout ensures our API doesn't hang forever if OpenSky goes down
        response = requests.get(OPENSKY_URL, params=params, timeout=10)
        response.raise_for_status() 
        data = response.json()

        # If there are no flights in the area, OpenSky returns null for 'states'
        if not data or not data.get("states"):
            return []

        clean_flights = []
        
        # OpenSky returns data as a raw list of values (to save bandwidth) rather than JSON keys.
        # We need to map these index positions to meaningful names for our AI later.
        for state in data["states"]:
            flight = {
                "icao24": state[0], # Unique aircraft identifier
                "callsign": state[1].strip() if state[1] else "UNKNOWN", # e.g., "UAL123"
                "origin_country": state[2],
                "longitude": state[5],
                "latitude": state[6],
                "altitude_meters": state[7],
                "velocity_m_s": state[9],
                "heading_degrees": state[10] # True track direction
            }
            
            # We only care about flights transmitting valid positional data
            if flight["longitude"] is not None and flight["latitude"] is not None:
                clean_flights.append(flight)
                
        return clean_flights

    except requests.exceptions.RequestException as e:
        # In a production app, we would log this error. For now, we print it.
        print(f"Error fetching OpenSky data: {e}")
        return None