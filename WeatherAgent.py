import logging
from dotenv import load_dotenv
from livekit.agents import JobContext, WorkerOptions, cli, function_tool, RunContext
from livekit.agents.voice import Agent, AgentSession
from livekit.plugins import silero
import requests
import os

load_dotenv('.env')

logging.getLogger("livekit.agents").setLevel(logging.ERROR)
logging.getLogger().setLevel(logging.ERROR)


class WeatherListenAndRespondAgent(Agent):
    def __init__(self) -> None:
        # You are a helpful agent. When the user speaks, you listen and respond.
                # When the user asks about weather, call the weather tool.
                # You are a helpful weather voice assistant. 
                # Returns weather temperature and cloud information if needed with some remarks.
        super().__init__(
            instructions="""
                You are a friendly, conversational weather assistant.
                Your job:
                - When the user asks about the current weather in a city, call the tool `get_weather`.
                - When the user asks about tomorrow or any future weather, call the tool `get_weather_forecast`.
                Your response style:
                - Speak naturally and warmly, like a helpful voice assistant.
                - Keep answers short, clear, and friendly.
                - Never mention tools, APIs, JSON, coordinates, or internal steps.
                - Never explain how you got the weather—just give the answer.
                - If the tool returns text, relay it directly in a natural spoken style.
                - If the user switches cities, smoothly give the new weather without repeating past context.
                - Give remarks based on the weather.
                Rules:
                - If the user asks anything weather-related, always use the appropriate tool.
                - For questions about “today”, “right now”, “currently” → use `get_weather`.
                - For questions with “tomorrow”, “next week”, “later”, “forecast” → use `get_weather_forecast`.
                - If the tool returns an error message, repeat it politely.
                - Never ask the user to specify the city again unless it's truly missing.
            """,
            stt="assemblyai/universal-streaming",
            llm="openai/gpt-4.1-mini",
            tts="cartesia/sonic-2:6f84f4b8-58a2-430c-8c79-688dad597532",
            vad=silero.VAD.load(),
        )


    @function_tool
    async def get_weather(self,context:RunContext,city: str)->any:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        r = requests.get(url)
        data = r.json()
        # print(data)
        if data.get("cod") != 200:
            return f"Sorry, I could not find weather for {city}."

        # weather = data["weather"][0]["description"]
        # temp = data["main"]["temp"]
        # feels = data["main"]["feels_like"]

        return data
    

    @function_tool
    async def get_weather_forcast(self,context:RunContext,city: str)->any:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&metric&cnt=3"
        r = requests.get(url)
        data = r.json()
        if int(data.get("cod")) != 200:
            print("problem")
            return f"Sorry, I could not find weather for {city}."

        return data
    
    async def on_enter(self):
        self.session.generate_reply()


async def entrypoint(ctx: JobContext):
    session = AgentSession()

    await session.start(
        agent=WeatherListenAndRespondAgent(),
        room=ctx.room
    )

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))