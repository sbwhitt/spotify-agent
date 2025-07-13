import os
import spotipy
import lyricsgenius

from strands import tool
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from ddgs import DDGS

def _init_spotipy(auth=False) -> spotipy.Spotify:
    if auth:
        return spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=os.environ["SPOTIFY_CLIENT_ID"],
                client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
                username=os.environ["SPOTIFY_USERNAME"],
                redirect_uri=os.environ["SPOTIFY_REDIRECT_URL"],
                scope="user-modify-playback-state",
            )
        )
    else:
        return spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=os.environ["SPOTIFY_CLIENT_ID"],
                client_secret=os.environ["SPOTIFY_CLIENT_SECRET"]
            )
        )

def _init_genius() -> lyricsgenius.Genius:
    return lyricsgenius.Genius(
        access_token=os.environ["GENIUS_ACCESS_TOKEN"]
    )

@tool
def spotify_track_search(query: str):
    """
    Performs a web search against the spotify catalog for tracks with name matching the provided query.
    A 'track' is also called a song.
    The tracks' spotify uris, names, albums, and artists will be returned in the results.

    Args:
        query (str): Song search query
    
    Returns:
        search_results (list): List of search results in the format: 
        [{track_uri: str, track_name: str, album: str, artists: list[str]}]
    """
    spot = _init_spotipy()
    res = spot.search(query, limit=5, type="track")
    tracks = []
    for item in res["tracks"]["items"]:
        artists = [a["name"] for a in item["artists"]]
        tracks.append({
            "track_uri": item["uri"],
            "track_name": item["name"],
            "album": item["album"]["name"],
            "artists": artists
        })
    return tracks

@tool
def spotify_album_search(query: str):
    """
    Performs a web search against the spotify catalog for albums with names matching the provided query.
    This tool only provides information about albums, not tracks within albums.
    Prioritize results that resemble the oldest and original versions of albums unless directed otherwise.
    The albums' spotify uris, names, total number of tracks, and artists will be returned in the results.

    Args:
        query (str): Album search query
    
    Returns:
        albums (list): List of album results in the format: 
        [{album_uri: str, album_name: str, total_tracks: int, artists: list[str]}]
    """
    spot = _init_spotipy()
    res = spot.search(query, limit=5, type="album")
    albums = []
    for item in res["albums"]["items"]:
        artists = [
            a["name"] for a in item["artists"]
        ]
        albums.append({
            "album_uri": item["uri"],
            "album_name": item["name"],
            "total_tracks": item["total_tracks"],
            "artists": artists
        })
    return albums

@tool
def spotify_album_tracks(album_uri: str) -> list:
    """
    Collects and returns the tracks associated with the provided album URI from the Spotify catalog.
    The tracks and their spotify URIs, names, and artists will be returned in the results.

    Args:
        album_uri (str): Spotify album URI
    
    Returns:
        tracks (list): List of tracks in the format: 
        [{track_uri: str, track_name: str, artists: list[str]}]
    """
    spot = _init_spotipy()
    res = spot.album_tracks(album_uri)
    tracks = []
    for item in res["items"]:
        artists = [a["name"] for a in item["artists"]]
        tracks.append({
            "track_uri": item["uri"],
            "track_name": item["name"],
            "artists": artists
        })
    return tracks

@tool
def spotify_play_track(track_uri: str) -> bool:
    """
    Plays the track associated with the provided track uri on the current user's spotify account.

    Args:
        track_uri (str): The uri of the track to play.

    Returns:
        True if the call succeeded, False if an error occured
    """
    try:
        spot = _init_spotipy(auth=True)
        spot.start_playback(uris=[track_uri])
        return True
    except Exception as e:
        print(e)
        return False

@tool
def genius_song_search(title: str, artist=None) -> str:
    """
    Searches for the provided song title and artist using the Genius song lyrics platform.

    Args:
        song (str): The title of the song to search for
        artist (str | None): The name of the song's artist (default None)

    Returns:
        lyrics (str | None): The song's lyrics if the search is successful, else None
    """
    try:
        genius = _init_genius()
        res = genius.search_song(title=title, artist=artist)
        return res.lyrics
    except:
        return None

@tool
def web_search(query: str) -> list[dict]:
    """
    Searches the web for the provided query using the Duck Duck Go search engine.
    Returns a list of the most relevant results.

    Args:
        query (str): The provided search query

    Returns:
        results (list): Most relevant search results in the format:
        [{title: str, href: str, body: str}]
    """
    res = DDGS().text(query, num_results=5)
    return res
