"""
Find tracks that are in multiple of your playlists.
You can give a list of regular expressions as patterns for playlist names
to ignore.

A config.ini, containing username,  client_id, client_secret and
redirect_uri needs to be present.
"""
import sys
from collections import defaultdict
import re

from helper import log_setup, track_to_str, playlist_to_str, get_client, item_loop
import logging

LOG = logging.getLogger(__name__)


def main(ignore_patterns):
    sp = get_client()
    results = defaultdict(list)
    playlists = sp.current_user_playlists()
    for playlist in item_loop(sp, playlists):
        playlist_str = playlist_to_str(playlist)
        if any(re.search(p, playlist_str) for p in ignore_patterns):
            LOG.info(f"Skipped {playlist_str}")
            continue

        pl_content = sp.playlist(playlist['id'], fields="tracks,next")
        for track in item_loop(sp, pl_content['tracks'], 'track'):
            results[track_to_str(track)].append(playlist_to_str(playlist))

    print_results(results)


def print_results(results):
    LOG.info("Duplicate Tracks:")
    for track, playlists in results.items():
        if len(playlists) > 1:
            LOG.info(track)
            for playlist in playlists:
                LOG.info(f"  {playlist}")
            LOG.info('')


if __name__ == '__main__':
    log_setup()
    try:
        ignore = sys.argv[1:]
    except IndexError:
        ingore = []

    main(ignore)
