import sys
import asyncio

from strands import Agent
from strands.models.ollama import OllamaModel
from tools import (
    spotify_track_search,
    spotify_album_search,
    spotify_album_tracks,
    spotify_play_track
)

ollama_model = OllamaModel(
    host="http://localhost:11434",
    model_id="qwen3:1.7b"
)

system_prompt = """
    You are a robot assistant that provides answers to requests using the provided tools.
    Do not be overly verbose in your reasoning or responses.
    Make sure to only pass valid URIs to tools that expect them. Do not pass placeholder inputs by accident.
"""

def handle_event(event: dict):
    if "data" in event:
        print(event["data"], end="")
    elif "current_tool_use" in event and event["current_tool_use"].get("name"):
        print(f"\nUSING TOOL: {event["current_tool_use"]["name"]}")
        print(f"with inputs: {event["current_tool_use"]["input"]}")
        print()

agent = Agent(
    model=ollama_model,
    tools=[
            spotify_track_search,
            spotify_album_search,
            spotify_album_tracks,
            spotify_play_track
    ],
    callback_handler=None,
    system_prompt=system_prompt
)

async def process_streaming_response(prompt: str):
    agent_stream = agent.stream_async(prompt)
    async for event in agent_stream:
        handle_event(event)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No prompt provided. Exiting.")

    asyncio.run(
        process_streaming_response(sys.argv[1])
    )
