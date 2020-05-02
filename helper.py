import logging
import sys
from configparser import ConfigParser

import spotipy
import spotipy.util as util


def log_setup(level=logging.INFO):
    """ Set up a basic logger. """
    logging.basicConfig(
        stream=sys.stdout,
        level=level,
        # format="%(levelname)7s | %(message)s | %(name)s"
        format="%(message)s"
    )


def get_username_and_client():
    """ Returns username from config and spotipy client. """
    parser = ConfigParser()
    parser.read('config.ini')
    cfg = lambda x: parser.get("DEFAULT", x)
    username = cfg('username')
    token = util.prompt_for_user_token(username,
                                       client_id=cfg('client_id'),
                                       client_secret=cfg('client_secret'),
                                       redirect_uri=cfg('redirect_uri'),
                                       )
    if not token:
        raise IOError(f"Can't get token for {username}")
    return username, spotipy.Spotify(auth=token)


def track_to_str(track):
    return (f"{track['name']} - "
            f"{', '.join(a['name'] for a in track['artists'])}")


def playlist_to_str(playlist):
    return playlist['name']