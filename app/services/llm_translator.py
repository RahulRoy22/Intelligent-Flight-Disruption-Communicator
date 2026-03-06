import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load the API key from our .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Use Gemini 2.5 Flash
model = genai.GenerativeModel('gemini-2.0-flash-exp')

def translate_weather_to_english(raw_metar: str) -> str:
    """
    Takes a raw METAR string and uses an LLM to explain it simply to a passenger.
    """
    system_prompt = """
    You are an empathetic, professional airline customer service agent.
    Your job is to read raw METAR aviation weather data and explain to a passenger 
    what the weather is currently like at the airport.
    
    Rules:
    - Keep it strictly to 1 or 2 short sentences.
    - Do NOT use any aviation jargon or acronyms.
    - Be comforting and clear.
    - Do not mention the word "METAR".
    """
    
    # Combine our system rules with the dynamic data
    full_prompt = f"{system_prompt}\n\nHere is the current weather data: {raw_metar}"
    
    try:
        response = model.generate_content(full_prompt)
        return response.text.strip()
    except Exception as e:
        print(f"LLM Error: {e}")
        return "We are currently unable to translate the local weather conditions."