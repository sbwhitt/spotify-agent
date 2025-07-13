import sys
import asyncio
import dotenv

from strands import Agent
from agents import spotify, lyrics
from utils import get_ollama_model

dotenv.load_dotenv()

def handle_event(event: dict):
    if "data" in event:
        print(event["data"], end="")
    elif "current_tool_use" in event and event["current_tool_use"].get("name"):
        print(f"\nUSING TOOL: {event["current_tool_use"]["name"]}")
        print(f"with inputs: {event["current_tool_use"]["input"]}")
        print()

async def process_streaming_response(agent: Agent, prompt: str):
    agent_stream = agent.stream_async(prompt)
    async for event in agent_stream:
        handle_event(event)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No prompt provided. Exiting.")

    system_prompt = """
        You are an orchestrator agent that queries specialized agents to answer music related requests.
        You will help the user search for songs and albums, play music, and read song lyrics.
        Break down the user's request into sub-queries and then pass them to the specialized agents.
        Once you receive a response from a specialized agent, determine if it satifies the request before concluding.
        
        You have access to the following specialized agents:
        - spotify tool: for searching and playing tracks, albums, etc. through spotify
        - lyrics tool: for searching info about a song's lyrics

        Be specific with your queries to the specialized agents. If you do not provide enough context the agents will not return good info.
        Use as much information from the user's request as possible in your queries to the agents.
        Do not provide any additional output besides the answer to the user's request.
        Do not attempt to provide song lyrics/info without a primary source. 
    """

    orchestrator = Agent(
        get_ollama_model(),
        tools=[
            spotify,
            lyrics
        ],
        system_prompt=system_prompt,
        callback_handler=None
    )

    asyncio.run(
        process_streaming_response(orchestrator, sys.argv[1])
    )
