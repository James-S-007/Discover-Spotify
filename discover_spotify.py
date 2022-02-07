import json
from pprint import pprint
from time import sleep
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CACHE_PLAYLIST_NAME = 'Discover Spotify Cache'
REDIRECT_URI = 'http://localhost:8080'
SCOPE = 'user-library-modify user-library-read playlist-modify-public playlist-modify-private playlist-read-private'  # TODO: Find what scopes are actually needed

def main():
    # get client_id and client_secret (currently stored in untracked json file, will change later)
    with open('client_keys.json') as f:
        data = json.load(f)
        CLIENT_ID = data['CLIENT_ID']
        CLIENT_SECRET = data['CLIENT_SECRET']

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI))
    cache_playlist = create_playlist_cache(sp)
    # get_all_user_playlists(sp)
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
    playlists = get_all_user_playlists(sp_client)
    user = sp_client.current_user()
    for playlist_id, playlist_name in playlists.items():
        if playlist_name == CACHE_PLAYLIST_NAME:
            return sp_client.user_playlist(user['id'], playlist_id)
    if not cache_playlist_id:
        return sp_client.user_playlist_create(user['id'], name=CACHE_PLAYLIST_NAME, public=False, collaborative=False, description='')  # TODO(James): Add err handling

# Creates dictionary of playlist_id : playlist_name for all user's playlists
def get_all_user_playlists(sp_client):
    num_playlists = 50
    limit = 50
    offset = 0
    user_playlists = {}
    while num_playlists == limit:
        results = sp_client.current_user_playlists(limit=limit, offset=offset)
        user_playlists = {**user_playlists, **{result['id'] : result['name'] for result in results['items']}}
        num_playlists = len(results['items'])
        offset += num_playlists
    return user_playlists

# TODO
def get_all_user_tracks(sp_client):
    tracks = {}  # dictionary of uri : track name
    num_playlists = 50
    limit = 50
    offset = 0
    while num_playlists == limit:
        results = sp.client.current_user_playlists(limit=limit, offset=offset)
        for result in results['items']:
            if result['uri'] not in tracks:
                tracks[result['uri']] = result['name']
        num_playlists = len(results['items'])
        offset += num_playlists


if __name__ == '__main__':
    main()
