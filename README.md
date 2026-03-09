# ✈️ Intelligent Flight Disruption Communicator

An AI-powered API that translates complex aviation weather data (METAR) into passenger-friendly disruption alerts using **RAG (Retrieval-Augmented Generation)** architecture.

## 🎯 What It Does

Converts this:
```
METAR KJFK 061551Z 04012KT 10SM OVC012 05/02 A3036
```

Into this:
```
"It's currently a bit chilly at the airport with a light wind, 
and the sky is completely covered with clouds. The visibility 
is still good, so it shouldn't impact your travel plans."
```

## 🏗️ Architecture

- **FastAPI** - High-performance REST API
- **ChromaDB** - Vector database for airport operational rules
- **Groq (Llama 3.3)** - Ultra-fast LLM for natural language generation
- **OpenSky Network** - Live flight tracking data
- **CheckWX API** - Real-time METAR weather data

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Groq API Key ([Get one free](https://console.groq.com))

### Installation

1. Clone the repository
```bash
git clone https://github.com/RahulRoy22/Intelligent-Flight-Disruption-Communicator.git
cd Intelligent-Flight-Disruption-Communicator
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Create `.env` file
```bash
GROQ_API_KEY=your_groq_api_key_here
```

4. Run the server
```bash
uvicorn app.main:app --reload
```

5. Open API docs at `http://localhost:8000/docs`

## 📡 API Endpoints

### Health Check
```bash
GET /health
```

### Live Flights (NYC Area)
```bash
GET /api/flights/live
```

### Weather Data
```bash
GET /api/weather/KJFK
```

### AI Weather Explanation
```bash
GET /api/weather/KJFK/explain
```

### Search Airport Rules
```bash
GET /api/rules/search?query=wind gusts KJFK
```

### 🔥 Master RAG Endpoint
```bash
GET /api/disruption/KJFK/explain
```
Combines live weather + vector DB rules + AI generation for complete disruption alerts.

## 🧠 How RAG Works Here

1. **Retrieval**: Fetch live METAR weather data
2. **Augmentation**: Query ChromaDB for relevant airport operational rules
3. **Generation**: Use Groq LLM to create passenger-friendly explanation

## 📁 Project Structure

```
flight_communicator/
├── app/
│   ├── main.py                 # FastAPI routes
│   └── services/
│       ├── opensky.py          # Flight tracking
│       ├── weather.py          # METAR data
│       ├── llm_translator.py   # Groq LLM integration
│       └── vector_store.py     # ChromaDB operations
├── requirements.txt
├── .env
└── .gitignore
```

## 🔑 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Groq API key for LLM | Yes |

## 🛠️ Tech Stack

- **FastAPI** - Modern Python web framework
- **ChromaDB** - Embedded vector database
- **Groq** - Fastest LLM inference platform
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation

## 📊 Example Response

```json
{
  "status": "success",
  "station": "KJFK",
  "backend_diagnostics": {
    "live_weather_used": "METAR KJFK 061551Z 04012KT 10SM OVC012 05/02 A3036",
    "database_rule_retrieved": "KJFK RULE: Visibility below 1/2 statute mile..."
  },
  "passenger_notification": "Current weather conditions at JFK may cause minor delays..."
}
```

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

## 📝 License

MIT

## 👤 Author

**Rahul Roy**
- GitHub: [@RahulRoy22](https://github.com/RahulRoy22)

---

⭐ Star this repo if you find it useful!
