import spotipy
from spotipy.oauth2 import SpotifyOAuth
import tkinter as tk
from tkinter import ttk, messagebox

# Replace with your credentials
client_id = "CLIENT_ID"
client_secret = "CLIENT_SECRET"

# Spotify OAuth setup
scope = "user-library-read playlist-read-private playlist-modify-public playlist-modify-private"
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
            # Skip local tracks
            if track['uri'].startswith('spotify:local:'):
                continue

            # Create a unique identifier for the track
            track_name = track["name"]
            track_artists = ", ".join([artist["name"] if artist["name"] else "" for artist in track["artists"]])
            track_duration = track["duration_ms"]
            track_identifier = (track_name, track_artists, track_duration)

            if track_identifier in seen_tracks:
                duplicates.append(track)
            else:
                seen_tracks.add(track_identifier)
    return duplicates

def deduplicate_playlist(playlist_id, playlist_name):
    print("Checking playlist:", playlist_name)
    all_tracks = []

    # Get playlist tracks
    all_tracks = get_playlist_tracks(playlist_id)

    # Add saved tracks to the list
    all_tracks = add_saved_tracks(all_tracks)

    # Identify duplicates within the playlist
    duplicates = get_duplicates(all_tracks)

    # Remove duplicates from the playlist
    if duplicates:
        for track in duplicates:
            track_uri = track["uri"]
            sp.playlist_remove_all_occurrences_of_items(playlist_id, [track_uri])
        print(f"Removed {len(duplicates)} duplicate tracks from playlist {playlist_name}")

    # Print results for the playlist
    print("Found", len(duplicates), "duplicate tracks in playlist", playlist_name)
    for track in duplicates:
        print(track["name"], "-", track["artists"][0]["name"])

    messagebox.showinfo("Deduplication Complete", f"Found and removed {len(duplicates)} duplicate tracks in playlist {playlist_name}")

def on_deduplicate():
    selected_playlist = playlist_combobox.get()
    if selected_playlist:
        playlist_id = playlist_dict[selected_playlist]
        deduplicate_playlist(playlist_id, selected_playlist)
    else:
        messagebox.showwarning("No Playlist Selected", "Please select a playlist to deduplicate.")

# Get all playlists (including private)
playlists = sp.current_user_playlists(limit=50)
playlist_dict = {playlist['name']: playlist['id'] for playlist in playlists['items']}

while playlists['next']:
    playlists = sp.next(playlists)
    playlist_dict.update({playlist['name']: playlist['id'] for playlist in playlists['items']})

# GUI setup
root = tk.Tk()
root.title("Spotify Playlist Deduplicator")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(frame, text="Select Playlist:").grid(row=0, column=0, padx=5, pady=5)
playlist_combobox = ttk.Combobox(frame, values=list(playlist_dict.keys()), state="readonly")
playlist_combobox.grid(row=0, column=1, padx=5, pady=5)

deduplicate_button = ttk.Button(frame, text="Deduplicate", command=on_deduplicate)
deduplicate_button.grid(row=1, column=0, columnspan=2, pady=10)

root.mainloop()