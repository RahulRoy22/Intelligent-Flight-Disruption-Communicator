import os
from groq import Groq
from dotenv import load_dotenv

# Load the API key from our .env file
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Initialize the Groq client
client = Groq(api_key=api_key)

def translate_weather_to_english(raw_metar: str) -> str:
    """
    Takes a raw METAR string and uses Groq (Llama 3) to explain it simply to a passenger.
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
    
    try:
        # We will use Llama 3 8B. It is incredibly fast and smart enough for this task.
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": f"Here is the current weather data: {raw_metar}",
                }
            ],
            model="llama-3.1-8b-instant", 
            temperature=0.3, # A lower temperature keeps the AI factual and prevents hallucinations
        )
        
        return chat_completion.choices[0].message.content.strip()
        
    except Exception as e:
        import traceback
        print("\n" + "="*40)
        print("🚨 GROQ ERROR DETECTED 🚨")
        print(f"Error Details: {e}")
        print(traceback.format_exc())
        print("="*40 + "\n")
        return "We are currently unable to translate the local weather conditions."


def explain_flight_disruption(raw_metar: str, airport_rule: str) -> str:
    """
    The RAG Engine: Combines live weather and retrieved airport rules to provide a status update.
    """
    system_prompt = """
    You are an empathetic airline customer service agent communicating with a passenger.
    Your job is to provide a flight status update based STRICTLY on the provided weather and operational rules.
    
    Guidelines:
    - If the operational rule states "Normal operations", inform the passenger their flight is proceeding on time with good weather.
    - If a specific disruption rule is provided, explain the delay empathetically.
    - NEVER invent or hallucinate reasons for a delay (like mechanical issues). Only use the provided context.
    - Keep it to 1 or 2 short sentences.
    - Do NOT use aviation jargon (like METAR, knots, or runway numbers).
    """
    
    user_prompt = f"Current Weather: {raw_metar}\nAirport Operational Rule: {airport_rule}\n\nPlease provide the passenger with their status update."
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="llama-3.1-8b-instant",
            temperature=0.1, # Dropping temperature even lower to strictly enforce factual reporting
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Groq RAG Error: {e}")
        return "We are currently checking your flight status. Please hold."