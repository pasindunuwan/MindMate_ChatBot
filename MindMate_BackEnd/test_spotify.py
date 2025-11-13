import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=r"E:\MainProjectFile\MindMate ChatBot\MindMate_BackEnd\.env")
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv('SPOTIFY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')
))
results = sp.search(q="calm instrumental playlist", type="playlist", limit=1)
print(results)