import sys
print(sys.executable)
print(sys.path)
from fastapi import FastAPI, HTTPException
from app.services.opensky import get_live_flights
from app.services.weather import get_current_weather  # Import our new service
from app.services.llm_translator import translate_weather_to_english

app = FastAPI(
    title="Intelligent Flight Disruption Communicator",
    description="API for translating raw aviation data into human-readable disruption alerts.",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "flight_communicator"}

@app.get("/api/flights/live")
async def fetch_live_flights():
    lamin, lamax = 40.5, 41.2
    lomin, lomax = -74.5, -73.0
    flights = get_live_flights(lamin, lamax, lomin, lomax)
    if flights is None:
        raise HTTPException(status_code=503, detail="OpenSky API is currently unavailable.")
    return {"status": "success", "airspace": "New York Metro", "sample_data": flights[:5]}

# --- NEW ROUTE BELOW ---

@app.get("/api/weather/{station_id}")
async def fetch_weather(station_id: str):
    """
    Test endpoint to fetch live weather (METAR) for a 4-letter ICAO airport code.
    """
    # Force uppercase because aviation codes are always uppercase
    weather_data = get_current_weather(station_id.upper())
    
    if weather_data is None:
        raise HTTPException(status_code=404, detail=f"Weather data not found for station {station_id}")
        
    return {
        "status": "success",
        "data": weather_data
    }

@app.get("/api/weather/{station_id}/explain")
async def explain_weather(station_id: str):
    """
    Fetches live weather for an airport and uses AI to explain it in plain English.
    """
    # 1. Fetch the raw data
    weather_data = get_current_weather(station_id.upper())
    
    if weather_data is None:
        raise HTTPException(status_code=404, detail="Weather data not found.")
        
    raw_metar = weather_data["raw_metar"]
    
    # 2. Translate it using our LLM
    explanation = translate_weather_to_english(raw_metar)
    
    return {
        "status": "success",
        "station": station_id.upper(),
        "raw_data": raw_metar,
        "ai_explanation": explanation
    }