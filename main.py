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
    "What date would you like the top 100 songs for? (YYYY-MM-DD): ")
response = requests.get("https://billboard.com/charts/hot-100/" + user_date)
soup = BeautifulSoup(response.text, "html.parser")

artist_list = [title.getText().strip("\n").replace(" Featuring", ",").replace(" &", ",")
               for title in soup.select("span.c-label.a-no-trucate")]
titles_list = [title.getText().strip("\n")
               for title in soup.select("li h3")][:100]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=SPOTIPY_REDIRECT_URI,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

song_urls = []
for i in range(100):
    track_info = sp.search(
        q=f"{titles_list[i]} {artist_list[i]}", type="track")
    try:
        url = track_info["tracks"]["items"][0]["uri"].split(":")[2]
        song_urls.append(url)
    except IndexError:
        print(
            f"{titles_list[i]} by {artist_list[i]} does not exist on Spotify. Skipped.")

playlist = sp.user_playlist_create(
    user=sp.current_user()["id"],
    name=f"{user_date} Billboard 100",
    description=f"Billboard top 100 from the date: {user_date}.",
    public=False
)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_urls)
