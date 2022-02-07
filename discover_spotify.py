import json
from pprint import pprint
from time import sleep
import spotipy
from spotipy.oauth2 import SpotifyOAuth

REDIRECT_URI = 'http://localhost:8080'
CACHE_PLAYLIST_NAME = 'Discover Spotify Cache'

def main():
    # get client_id and client_secret (currently stored in untracked json file, will change later)
    with open('client_keys.json') as f:
        data = json.load(f)
        CLIENT_ID = data['CLIENT_ID']
        CLIENT_SECRET = data['CLIENT_SECRET']

    scope = 'user-library-modify user-library-read playlist-modify-public playlist-modify-private playlist-read-private'  # TODO: Find what scopes are actually needed

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI))
    cache_playlist = create_playlist_cache(sp)
    # update cache playlist with new songs from other playlists
    

def print_playlist_categories(sp_client):
    categories = sp_client.categories()
    for item in categories['categories']['items']:
        print(item['name'])

def get_current_user_playlists(sp_client, limit=50, offset=0):
    results = sp_client.current_user_playlists(limit=limit, offset=offset)
    for idx, item in enumerate(results['items']):
        playlist = item['name']
        print(f'{idx+offset+1}: {playlist}')
    return results['items']

def get_recommendations(sp_client):
    results = sp_client.recommendations(seed_artists=['6d24kC5fxHFOSEAmjQPPhc'], seed_genres=['metal'], seed_tracks=['56g7gV4V3YvAmo4zbwnh3j'])
    for key in results:
        print(key)
    for result in results['tracks']:
        print(result['name'])

# Creates a private cache playlist if it does not already exist
# Returns playlist
def create_playlist_cache(sp_client):
    cache_playlist_id = None
    num_playlists = 50
    limit = 50
    offset = 0
    while num_playlists == limit and not cache_playlist_id:
        results = sp_client.current_user_playlists(limit=limit, offset=offset)
        for result in results['items']:
            if result['name'] == CACHE_PLAYLIST_NAME:
                return result
        num_playlists = len(results['items'])
        offset += num_playlists
    user = sp_client.current_user()
    if not cache_playlist_id:
        return sp_client.user_playlist_create(user['id'], name=CACHE_PLAYLIST_NAME, public=False, collaborative=False, description='')  # TODO(James): Add err handling

if __name__ == '__main__':
    main()
