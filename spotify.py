import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def spotify_playlist(playlist_name, client_id, client_secret):
    # Initialize the Spotipy object
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

    # Get the playlist with the given name
    playlists = sp.user_playlists('1137628596')
    playlist = None
    while playlists:
        for i, pl in enumerate(playlists['items']):
            if pl['name'] == playlist_name:
                playlist = pl
                break
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            break

    # Get the songs from the playlist
    songs_list = []
    if playlist:
        results = sp.playlist_items(playlist['id'], fields="items.track.name,items.track.artists")
        for item in results['items']:
            track_name = item['track']['name']
            artist_name = item['track']['artists'][0]['name']
            songs_list.append(f"{artist_name} - {track_name}")
        return songs_list
    else:
        print(f"No playlist found with the name '{playlist_name}'")
        return None
