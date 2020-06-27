import os
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint
from time import sleep

username = "aglalit"
scope = "user-read-currently-playing,user-read-playback-state,user-modify-playback-state"
redirect_uri = "http://localhost:8888/callback"

token = util.prompt_for_user_token(username, scope, os.environ['SPOTIPY_CLIENT_ID'], os.environ['SPOTIPY_CLIENT_SECRET'], redirect_uri)

sp = spotipy.Spotify(auth=token)

results = sp.search(q='weezer', limit=20)
for idx, track in enumerate(results['tracks']['items']):
    print(idx, track['name'])
    

# Shows playing devices
res = sp.devices()
pprint(res)

# Change track
sp.start_playback(uris=['spotify:track:6gdLoMygLsgktydTQ71b15'])

# Change volume
sp.volume(100)
sleep(2)
sp.volume(50)
sleep(2)
sp.volume(100)                    