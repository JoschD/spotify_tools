"""
Adds all of your saved albums into your queue or if either a
playlist name or id is given, to a playlist.
The songs are shuffled by (first-) artists, so that it plays an artist only again,
after all other artists were played.

If a playlist name is given the songs should be added to that playlist or
if no playlist is found, a new one is created.
The API seems to have some problems finding just recently created playlists,
so it might create a new playlist. In that case use the playlist_id directly.

A config.ini, containing username,  client_id, client_secret and
redirect_uri needs to be present.
"""
import sys
import time
from collections import defaultdict
import random

from spotipy.exceptions import SpotifyException
from helper import get_client, log_setup, track_to_str, playlist_to_str, item_loop, find_playlist_by_name
import logging


LOG = logging.getLogger(__name__)


def main(playlist_name=None):
    scope = 'user-library-read'
    if playlist_name:
        scope += ",playlist-modify-private,playlist-modify-public"
    else:
        scope += ",user-modify-playback-state"
    sp = get_client(scope=scope)
    results = defaultdict(list)
    albums = sp.current_user_saved_albums(limit=50, offset=0)
    for album in item_loop(sp, albums, 'album'):
        for track in item_loop(sp, album['tracks']):
            first_artist = track['artists'][0]['name']
            results[first_artist].append(track['id'])

    tracks_ids = shuffle_results(results)
    add_results(sp, tracks_ids, playlist_name)


def shuffle_results(results):
    track_ids = []
    for artist, tracks in results.items():
        random.shuffle(tracks)
        results[artist] = tracks

    artists = list(results.keys())
    while len(artists):
        random.shuffle(artists)

        for idx, artist in enumerate(artists):
            track_ids.append(results[artist].pop(0))
            if len(results[artist]) == 0:
                artists.pop(idx)

    return track_ids


def add_results(sp, track_ids, playlist_name=None):
    if playlist_name:
        try:
            playlist = sp.playlist(playlist_name)
        except SpotifyException:
            playlist = find_playlist_by_name(sp, playlist_name)

        if not playlist:
            playlist = create_playlist(sp, playlist_name)
        add_tracks(sp, playlist, track_ids)
    else:
        for id in track_ids:
            sp.add_to_queue(id)
            time.sleep(.005)  # trying to avoid API-rate limits


def add_tracks(sp, playlist, track_ids, n_at_once=20):
    user = sp.me()['id']
    for to_add in (track_ids[i:i+n_at_once] for i in range(0, len(track_ids), n_at_once)):
        sp.user_playlist_add_tracks(user, playlist['id'], to_add)
        time.sleep(.01)  # trying to avoid API-rate limits


def create_playlist(sp, playlist_name):
    user = sp.me()['id']
    return sp.user_playlist_create(
        user, playlist_name,
        public=False,
        description='Shuffled playlist from all your artists.')


if __name__ == '__main__':
    log_setup()
    try:
        pl_name = sys.argv[1]
    except IndexError:
        pl_name = None

    main(pl_name)
