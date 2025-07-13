# Spotify Agent

Uses `strands` and `ollama` to power an ai agent that answers questions related to music. The agent is capable of searching for and playing songs through the Spotify API, as well as looking up lyrics using the Genius API.

The model that I tested with was `qwen3:1.7b` from ollama.

Example prompts:
  * "play the third track off of the album moving pictures by rush"
  * "which album has more tracks, moving pictures by rush, or fly by night by rush"
  * "how many times do they say 'catch' in tom sawyer by rush"

Requires Spotify and Genius API credentials to access tools. API info is pulled from a top level .env file.

Example .env:

```
SPOTIFY_CLIENT_ID=<client_id>
SPOTIFY_CLIENT_SECRET=<client_secret>
SPOTIFY_REDIRECT_URL=http://127.0.0.1:8080
SPOTIFY_USERNAME=<your spotify username>

GENIUS_ACCESS_TOKEN=<access_token>
```
