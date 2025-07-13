from strands import Agent, tool
from utils import get_ollama_model
from tools import (
    spotify_track_search,
    spotify_album_search,
    spotify_album_tracks,
    spotify_play_track
)

@tool
def spotify(query: str):
    """
    This agent has access to tools that can search through the Spotify catalog as well as control playback.
    The agent has access to the following tools:

        * spotify_track_search - Search for a track by name, returns list of tracks
            * Example: 'Search for a track named <track name> by <artist>'
        * spotify_album_search - Search for an album by name, returns list of albums
            * Example: 'Search for an album named <album name> by <artist>'
        * spotify_album_tracks - Retrieve a list of tracks for the provided album
            * Example: 'What tracks are on the album, <album name>'
        * spotify_play_track - Plays the provided track through the user's Spotify account
            * Example: 'Play the track, <track name> by <artist>'

    Args:
        query (str): The request to be passed to the spotify agent

    Returns:
        agent_response (str): The response from the Spotify agent
    """
    system_prompt = """
        You are a specialized assistant that controls access to Spotify information.
        You have access to several tools that allow you to search the Spotify catalog and play tracks. 
        Make sure to only pass valid URIs to tools that expect them.
        Do not pass placeholder inputs by accident.
    """

    agent = Agent(
        model=get_ollama_model(),
        tools=[
                spotify_track_search,
                spotify_album_search,
                spotify_album_tracks,
                spotify_play_track
        ],
        system_prompt=system_prompt,
        callback_handler=None
    )
    res = agent(query)
    return str(res)
