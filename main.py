import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Replace with your credentials
client_id = "babdb7c4a1b1408faef67723898bf420"
client_secret = "f8da5bc913254379875719ea8319325a"

# Spotify OAuth setup
scope = "user-library-read playlist-read-private" 
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id, client_secret, redirect_uri="http://localhost:8080", scope=scope))

def get_playlist_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

def add_saved_tracks(tracks):
    saved_tracks = sp.current_user_saved_tracks()
    for item in saved_tracks['items']:
        tracks.append(item)
    while saved_tracks['next']:
        saved_tracks = sp.next(saved_tracks)
        for item in saved_tracks['items']:
            tracks.append(item)
    return tracks

def get_duplicates(tracks):
    seen_tracks = set()
    duplicates = []
    for track_data in tracks:
        # Handle tracks and saved tracks format difference
        if 'track' in track_data:
            track = track_data['track']
        else:
            track = track_data['item']['track']

        if track is not None:
            track_id = track["id"]
            if track_id in seen_tracks:
                duplicates.append(track)
            else:
                seen_tracks.add(track_id)
    return duplicates

def deduplicate_playlists(playlists):
    for playlist in playlists['items']:
        print("Checking playlist:", playlist['name'])
        all_tracks = []

        # Get playlist tracks
        all_tracks = get_playlist_tracks(playlist['id'])

        # Add saved tracks to the list
        all_tracks = add_saved_tracks(all_tracks)

        # Identify duplicates within the playlist
        duplicates = get_duplicates(all_tracks)

        # Print results for the playlist
        print("Found", len(duplicates), "duplicate tracks in playlist", playlist['name'])
        for track in duplicates:
            print(track["name"], "-", track["artists"][0]["name"])

# Get all playlists (including private)
playlists = sp.current_user_playlists(limit=50)

deduplicate_playlists(playlists)

while playlists['next']:
    playlists = sp.next(playlists)
    
deduplicate_playlists(playlists)

# # Loop through each playlist
# for playlist in playlists['items']:
#     print("Checking playlist:", playlist['name'])
#     all_tracks = []

#     # Get playlist tracks
#     results = sp.playlist_tracks(playlist['id'])
#     tracks = results['items']
#     while results['next']:
#         results = sp.next(results)
#         tracks.extend(results['items'])
#     all_tracks.extend(tracks) 

#     # Add saved tracks to the list
#     saved_tracks = sp.current_user_saved_tracks()
#     for item in saved_tracks['items']:
#         all_tracks.append(item)
#     while saved_tracks['next']:
#         saved_tracks = sp.next(saved_tracks)
#         for item in saved_tracks['items']:
#             all_tracks.append(item)

#     # Identify duplicates within the playlist
#     seen_tracks = set()
#     duplicates = []
#     for track_data in all_tracks:
#         # Handle tracks and saved tracks format difference
#         if 'track' in track_data:
#             track = track_data['track']
#         else:
#             track = track_data['item']['track']

#         if track is not None:
#             track_id = track["id"]
#             if track_id in seen_tracks:
#                 duplicates.append(track)
#             else:
#                 seen_tracks.add(track_id)

#     # Print results for the playlist
#     print("Found", len(duplicates), "duplicate tracks in playlist", playlist['name'])
#     for track in duplicates:
#         print(track["name"], "-", track["artists"][0]["name"])


