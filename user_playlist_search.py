"""
Searches for the key given as first commandline argument in the name and
artists of your tracks in your playlists and shows you in which playlists
these tracks are.

A config.ini, containing username,  client_id, client_secret and
redirect_uri needs to be present.
"""
import logging
import sys
from collections import defaultdict

from helper import get_client, log_setup, track_to_str, playlist_to_str, item_loop

LOG = logging.getLogger(__name__)


def main(to_find):
    sp = get_client()
    results = defaultdict(list)
    to_find = to_find.lower()
    playlists = sp.current_user_playlists()
    for playlist in item_loop(sp, playlists):
        pl_content = sp.playlist(playlist['id'], fields="tracks,next")
        for track in item_loop(sp, pl_content['tracks'], 'track'):
            if find_in_track(track, to_find):
                results[track_to_str(track)].append(playlist_to_str(playlist))

    print_results(results, to_find)


def find_in_track(track, to_find):
    if to_find in track['name'].lower():
        return True
    for artist in track['artists']:
        if to_find in artist['name'].lower():
            return True
    return False


def print_results(results, to_find):
    if not len(results):
        LOG.info(f"No Tracks found containing '{to_find}' in your playlists.")
    else:
        LOG.info(f"Found tracks containing '{to_find}' in your playlists:")
        LOG.info("")
        for track, playlists in results.items():
            LOG.info(track)
            for playlist in playlists:
                LOG.info(f"  {playlist}")
            LOG.info("")


if __name__ == '__main__':
    log_setup()
    try:
        key = sys.argv[1]
    except IndexError:
        raise IOError("Search key missing.\n"
                      "usage: python user_playlists_search.py [key]")
    else:
        main(key)
