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

from helper import get_username_and_client, log_setup, track_to_str, playlist_to_str
import logging

LOG = logging.getLogger(__name__)


def main(ignore_patterns):
    username, sp = get_username_and_client()
    results = defaultdict(list)
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:
        if playlist['owner']['id'] == username:
            playlist_str = playlist_to_str(playlist)
            if any(re.search(p, playlist_str) for p in ignore_patterns):
                LOG.info(f"Skipped {playlist_str}")
                continue
            pl_content = sp.playlist(playlist['id'], fields="tracks,next")
            tracks = pl_content['tracks']
            loop_tracks(results, tracks, playlist)
            while tracks['next']:
                tracks = sp.next(tracks)
                loop_tracks(results, tracks, playlist)

        print_results(results)


def loop_tracks(results, tracks, playlist):
    for item in tracks['items']:
        track = item['track']
        results[track_to_str(track)].append(playlist_to_str(playlist))


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
