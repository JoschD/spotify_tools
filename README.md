Spotify Scripts
===============================

Some scripts to provide some advanced spotify functionality, 
that should have come with the GUI but didn't.

## Search Functions
### User Playlist Search
Find out if a certain song is in your playlists and if so, in which ones.

Input is a part of the songs name or artist. <br>
Output are all songs found
in your playlist containing that part, including the names of the playlists
they are in.

Usage:
``` 
python user_playlist_search.py KEY
```
where `KEY` is the part of the song's name you are looking for.

### Find Duplicates
Finds songs that are in multiple of your playlists. <br>
All found songs are listed with the playlists they are in.

Optional regular expression patterns applied on playlist names
can be used to exclude playlists (i.e. they are 'ignore-patterns', not
'look-here-patterns').


Usage:
``` 
python find_duplicates.py [PATTERN] [PATTERN] ...
```
where `PATTERN` are regular expression patterns to exclude playlists from this
search.

## Shuffle Functions
### Album Artist Shuffle
Adds all of your saved albums into your queue or if either a 
playlist name or id is given, to a playlist.
The songs are shuffled by (first-) artists, so that it plays an artist only again,
after all other artists were played.

If a playlist name is given the songs should be added to that playlist or
if no playlist is found, a new one is created.
The API seems to have some problems finding just recently created playlists,
so it might create a new playlist. In that case use the playlist_id directly.

Problem: Artists with more songs will dominate the end of the queue.

Usage:
```
python album_artist_shuffle [playlist]
```


## Installation

These scripts are based on the [spotipy](https://github.com/plamere/spotipy)
spotify python API wrapper. So please make sure this package is installed in 
your python environment (e.g. via `pip install spotipy`)

Furthermore, I am not an api-developer and I have no idea how to distribute 
apps that require API-access. Hence you will have to setup 'your own' app.
It has two extra steps, but at least this way you are not giving access to your
spotify account to a random guy who tells you so in his github readme.

These steps are:

**Create an app**
 - Go to https://developer.spotify.com/dashboard 
 - Log in with your spotify account
 - Click on "CREATE AN APP" <br>
  (fill in name and usage as you please, be creative, 
  tell them you are not using it commercially, say you understand all the things)
 - After creation click on "EDIT SETTINGS"
 - add `http://localhost:9090` in "Redirect URIs" (don't forget to click "ADD")
 - on the main screen find the `Client ID` and `Client Secret` <br>
  and try to remember them by heart, you will need them later
 
 **Modify config.ini**
 - open your local copy of `config_example.ini`, 
 and fill in your spotify `username` as well as the `client_id` and `client_secret`
 from your just created app
 _(depending on how you registered in spotify `username` might not what you
  expect. You can figure it out by going to http://open.spotify.com and 
   clicking on the top right on your name and then on "Profile". The part 
   in the address now after `open.spotify.com/user/` should be your username/userid)_
 - rename `config_example.ini` to `config.ini` and have it in the folder you
 are running the scripts from
 
 
 ### ENJOY!
 Cheers, JD