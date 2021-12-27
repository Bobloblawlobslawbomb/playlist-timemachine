import os
from os.path import join, dirname
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.environ.get('SPOTIPY_REDIRECT_URL')


user_date = input(
    "What date would you lke the top 100 songs for? (YYYY-MM-DD): ")
response = requests.get("https://billboard.com/charts/hot-100/" + user_date)
soup = BeautifulSoup(response.text, "html.parser")
titles_list = [title.getText().strip("\n")
               for title in soup.select("li h3")][:100]

scope = "playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope=scope, redirect_uri=SPOTIPY_REDIRECT_URI, client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

results = sp.current_user()

print(results["display_name"])
