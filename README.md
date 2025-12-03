# Weather Voice Assistant

A real-time **voice-based weather assistant** built using the **LiveKit Agents Framework**.  
The assistant listens to the user, extracts the city name, calls the weather API, and responds naturally using TTS.

---

##  Features

###  Voice Interaction
- Real-time **speech-to-text** (AssemblyAI)
- Natural **text-to-speech** (Cartesia)
- **VAD** for voice activity detection (Silero)

###  Weather API Integration
- Uses **OpenWeatherMap** API
- Supports:
  - Current weather  
  - Short-term forecast
- Automatic city extraction via LLM
- Natural, human-friendly spoken responses

###  Intelligent Agent Behavior
- Built on **LiveKit Agents + GPT-4.1-mini**
- Understands queries like:
  - “What’s the weather in Mumbai?”
  - “How about Bangalore?”
  - “Will it rain tomorrow in Pune?”




## 🛠️ Setup & Installation

### 1. Clone the repository
``` bash
git clone https://github.com/Shubhamkumar90/WeatherAIAgent.git
cd WeatherAIAgent
```
### 2. Add environment variables
Create a .env file.

To get LIVEKIT keys, you have to create a account in <a href=https://livekit.io/>livekit</a> and create a project, then click on the project api key.
``` ini
OPENWEATHER_API_KEY=your_api_key
LIVEKIT_API_KEY=your_livekit_key
LIVEKIT_API_SECRET=your_key
LIVEKIT_URL=your_url
```
### 3. Install dependencies
```
pip install -r requirements.txt
```
### 4. Run the agent
``` bash
python WeatherAgent.py console
```

## How It Works

1. **User speaks**
2. **STT** converts speech → text  
3. **LLM** identifies intent + extracts city  
4. **Tool call** executed (`get_weather` or `get_weather_forecast`)  
5. **API** returns weather  
6. Weather is **formatted** into a friendly sentence  
7. **TTS** speaks the response  



##  Weather Tools

### `get_weather(city)`
Fetches current weather from OpenWeatherMap.

### `get_weather_forecast(city)`
Fetches forecast weather (e.g., tomorrow, next days).

