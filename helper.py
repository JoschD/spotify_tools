import logging
import sys
from configparser import ConfigParser

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth


def log_setup(level=logging.INFO):
    """ Set up a basic logger. """
    logging.basicConfig(
        stream=sys.stdout,
        level=level,
        # format="%(levelname)7s | %(message)s | %(name)s"
        format="%(message)s"
    )


def get_client(scope=None):
    """ Returns username from config and spotipy client. """
    parser = ConfigParser()
    parser.read('config.ini')
    cfg = lambda x: parser.get("DEFAULT", x)
    token = util.prompt_for_user_token(cfg('username'),
                                       scope=scope,
                                       client_id=cfg('client_id'),
                                       client_secret=cfg('client_secret'),
                                       redirect_uri=cfg('redirect_uri'),
                                       )
    if not token:
        raise IOError(f"Can't get token for {cfg('username')}")
    return spotipy.Spotify(auth=token)


def track_to_str(track):
    return (f"{track['name']} - "
            f"{', '.join(a['name'] for a in track['artists'])}")


def playlist_to_str(playlist):
    return playlist['name']


def item_loop(sp, looper, name=None):
    while True:
        for item in looper['items']:
            if name:
                yield item[name]
            else:
                yield item

        if not looper['next']:
            break

        looper = sp.next(looper)



