import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# ----------------------------------------------
# Generated Using ChatGPT 4o
# ----------------------------------------------

# -----------------------
# Configuration
# -----------------------

SETLIST_FM_API_KEY = 'your_setlistfm_api_key'
SPOTIFY_CLIENT_ID = 'your_spotify_client_id'
SPOTIFY_CLIENT_SECRET = 'your_spotify_client_secret'
SPOTIFY_REDIRECT_URI = 'http://localhost:8888/callback'
SPOTIFY_USERNAME = 'your_spotify_username'

# Example Setlist.fm URL: https://www.setlist.fm/setlist/coldplay/2023/wembley-stadium-london-england-7bb5b294.html
SETLIST_ID = '7bb5b294'  # You can extract this from the URL

# Playlist name
PLAYLIST_NAME = 'Coldplay Setlist - Wembley 2023'

# -----------------------
# Step 1: Fetch Setlist.fm data
# -----------------------

def get_setlist_songs(setlist_id):
    headers = {
        'Accept': 'application/json',
        'x-api-key': SETLIST_FM_API_KEY,
        'User-Agent': 'SetlistToSpotifyApp/1.0'
    }
    url = f'https://api.setlist.fm/rest/1.0/setlist/{setlist_id}'
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Setlist.fm API error: {response.status_code} - {response.text}")

    data = response.json()
    songs = []

    for set_item in data.get('sets', {}).get('set', []):
        for song in set_item.get('song', []):
            song_name = song.get('name')
            if song_name:
                songs.append(song_name)

    artist_name = data.get('artist', {}).get('name', 'Unknown Artist')
    return artist_name, songs

# -----------------------
# Step 2: Create Spotify Playlist and Add Songs
# -----------------------

def create_spotify_playlist(artist_name, track_list):
    scope = 'playlist-modify-public'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=scope,
        username=SPOTIFY_USERNAME
    ))

    user_id = sp.me()['id']
    playlist = sp.user_playlist_create(user=user_id, name=PLAYLIST_NAME, public=True)
    playlist_id = playlist['id']

    track_uris = []

    for track in track_list:
        results = sp.search(q=f'track:{track} artist:{artist_name}', type='track', limit=1)
        items = results['tracks']['items']
        if items:
            uri = items[0]['uri']
            track_uris.append(uri)
            print(f'Found: {track}')
        else:
            print(f'Not found: {track}')

    # Add in batches of 100
    for i in range(0, len(track_uris), 100):
        sp.playlist_add_items(playlist_id, track_uris[i:i+100])

    print(f"Playlist created: {playlist['external_urls']['spotify']}")

# -----------------------
# Run it all
# -----------------------

def main():
    artist, songs = get_setlist_songs(SETLIST_ID)
    print(f"Creating playlist for {artist} with {len(songs)} songs.")
    create_spotify_playlist(artist, songs)

if __name__ == '__main__':
    main()
