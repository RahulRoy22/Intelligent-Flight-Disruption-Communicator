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
            model="llama-3.3-70b-versatile", 
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
    The RAG Engine: Combines live weather and retrieved airport rules to explain a delay.
    """
    system_prompt = """
    You are an empathetic airline customer service agent. A passenger's flight is currently delayed.
    Your job is to explain exactly WHY it is delayed by combining the current weather and the airport's operational rules.
    
    Guidelines:
    - Keep it to 1 or 2 comforting sentences.
    - Do NOT use any aviation jargon (like METAR, knots, or runway numbers).
    - Explain the weather condition AND the specific action the airport is taking (e.g., plowing snow, spacing planes out).
    """
    
    # This is where the "Augmented" part of RAG happens. We inject our data into the prompt.
    user_prompt = f"Current Weather: {raw_metar}\nAirport Operational Rule: {airport_rule}\n\nPlease explain the delay to the passenger."
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="llama3-8b-8192",
            temperature=0.2, # Extremely low temperature so it relies heavily on our provided rule
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Groq RAG Error: {e}")
        return "Your flight is currently delayed due to local weather conditions. We will update you shortly."