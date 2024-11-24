# Spotify Playlist Deduplicator

This Python script uses the Spotipy library to identify and remove duplicate tracks from your Spotify playlists. It also considers your saved tracks when checking for duplicates, preventing re-adding songs already in your library.

## Features

-   **Duplicate detection:** Identifies duplicate tracks within a selected playlist based on track name, artist(s), and duration.
-   **Saved tracks integration:** Checks for duplicates against your saved tracks, preventing re-adding already saved songs.
-   **Local track handling:** Ignores local tracks to avoid issues with undefined metadata.
-   **User-friendly GUI:** Provides a simple Tkinter interface for playlist selection and deduplication initiation.
-   **Clear output:** Prints the number of duplicates found and removed for each playlist.

## Installation

1. **Install required libraries:**

    ```bash
    pip install spotipy tkinter
    ```

2. **Create a Spotify app:**

    - Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
    - Create a new app.
    - Add `http://localhost:8080` as a redirect URI under the "Edit Settings" section.

3. **Configure credentials:**
    - Replace `CLIENT_ID` and `CLIENT_SECRET` in the script with your app's credentials.

## Usage

1. **Run the script:**

    ```bash
    python main.py
    ```

2. **Authorize the app:**

    - A web browser will open prompting you to log in to your Spotify account and authorize the app.

3. **Select a playlist:**

    - Choose the playlist you want to deduplicate from the dropdown menu in the GUI.

4. **Click "Deduplicate":**
    - The script will analyze the selected playlist and remove any duplicate tracks.
    - A message box will appear confirming the deduplication process and the number of duplicates removed.
    - The console will also print detailed information about the duplicates found.

## How it works

1. **Fetches playlist tracks:** Retrieves all tracks from the selected playlist using the `get_playlist_tracks` function.

2. **Includes saved tracks:** Retrieves all saved tracks using the `add_saved_tracks` function and adds them to the list of tracks to check against.

3. **Identifies duplicates:** The `get_duplicates` function iterates through the combined track list and uses a set to track unique track identifiers (name, artists, duration). Tracks found more than once are marked as duplicates.

4. **Removes duplicates:** The `deduplicate_playlist` function removes all occurrences of duplicate tracks from the playlist using `sp.playlist_remove_all_occurrences_of_items`.

5. **Presents results:** Displays the number of duplicates found and removed in both the console and a message box.

## Contributing

Contributions are welcome! Feel free to submit pull requests for bug fixes, feature enhancements, or code improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
