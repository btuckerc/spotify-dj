
from __future__ import print_function    # (at top of module)
import os, sys, time, math, json, pprint, subprocess, requests
import spotipy
from oauth2 import SpotifyClientCredentials
import util
import simplejson as json
from tqdm import tqdm

scope = 'user-library-read, playlist-read-private'
USERNAME = os.getenv('SPOTIFY_USERNAME')
USER_TOKEN = os.getenv('USER_TOKEN')
token = util.prompt_for_user_token(USERNAME, scope)
print(token)

creds = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=creds)
sp.trace = False

url = "https://api.spotify.com/v1/me/tracks?limit=50&offset=0"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Bearer " + USER_TOKEN
}
total = requests.get(url, headers=headers).json()['total']
playlist = []
tempos = {}
offset = 0
for i, num in enumerate(tqdm(range(0,total,50))):# offset < total:
    url = "https://api.spotify.com/v1/me/tracks?limit=50&offset={}".format(num)
    songs = requests.get(url, headers=headers).json()['items']
    for j,t in enumerate((songs)):
        meta = {
            "uri": t['track']['uri'].encode("utf-8"),
            "name": t['track']['name'].encode("utf-8"),
            "popularity": t['track']['popularity'],
            "artists": ', '.join(i['name'] for i in t['track']['artists']).encode("utf-8")
        }
        features = sp.audio_features(t['track']['uri'])[0]
        playlist.append({**meta, **features})
        temp = str(int(features['tempo']/10)) + '0'
        if (temp in tempos):
            tempos[temp] += 1
        else:
            tempos[temp] = 1
    offset += 50

tempo = sorted(playlist, key=lambda k: (round(
    k['energy'], 1), int(k['tempo']/10), k['key']))
energy = sorted(playlist, key=lambda k: k['energy'])
hi = tempo[math.ceil(len(tempo)/2):]
hi1 = hi[0::2]
hi2 = hi[1::2]
lo = tempo[:math.floor(len(tempo)/2)]
lo1 = lo[0::2][::-1]
lo2 = lo[1::2]
sorted_tempo = hi1 + lo1 + lo2 + hi2
with open("tracks.txt", "w") as f:
    f.write("\n".join(list("{}\t{}\t{}\t{}\t{}".format(
        i['popularity'], i['key'], i['tempo'], i['energy'], i['name']) for i in sorted_tempo)))

# username
# playlist_name
# playlist_description
# playlists = sp.user_playlist_create(username, playlist_name,
#                                     playlist_description)
# pprint.pprint(playlists)

# results = sp.search(q='weezer', limit=20)
# for i, t in enumerate(results['tracks']['items']):
#     print(' ', i, t['name'])

#results = sp.current_user_playlists(limit=50)
# for i, item in enumerate(results['items']):
#     print("%d %s" % (i, item['name']))

'''
# shows acoustic features for tracks for the given artist

uri = 'spotify:user:{}:playlist:4GLMvYLD7N9TcQG9GgQG69'.format(USERNAME)
username = uri.split(':')[2]
playlist_id = uri.split(':')[4]

results = sp.user_playlist(username, playlist_id)
tempos = {}
playlist = []
for i, t in enumerate(tqdm(results['tracks']['items'])):
    meta = {
        "uri": t['track']['uri'],
        "name": t['track']['name'],
        "popularity": t['track']['popularity'],
        "artists": ', '.join(i['name'] for i in t['track']['artists'])
    }
    features = sp.audio_features(t['track']['uri'])[0]
    playlist.append({**meta, **features})
    temp = str(int(features['tempo']/10)) + '0'
    if (temp in tempos):
        tempos[temp] += 1
    else:
        tempos[temp] = 1

tempo = sorted(playlist, key=lambda k: (round(
    k['energy'], 1),int(k['tempo']/10), k['key']))
energy = sorted(playlist, key=lambda k: k['energy'])
hi = tempo[math.ceil(len(tempo)/2):]
hi1 = hi[0::2]
hi2 = hi[1::2]
lo = tempo[:math.floor(len(tempo)/2)]
lo1 = lo[0::2][::-1]
lo2 = lo[1::2]
# print(list(i['energy'] for i in (hi1 + lo1 + lo2 + hi2)))
sorted_tempo = hi1 + lo1 + lo2 + hi2

with open("cache/" + playlist_id + ".txt", "w") as f:
    f.write("\n".join(list("{}\t{}\t{}\t{}\t{}".format(
        i['popularity'], i['key'], i['tempo'], i['energy'], i['name']) for i in sorted_tempo)))
    print("\n".join(list("{}\t{}\t{}\t{}\t{}".format(
        i['popularity'], i['key'], i['tempo'], i['energy'], i['name']) for i in sorted_tempo)))
# for track in sorted_energy:
#     print(json.dumps(track, indent=4))
'''
print (json.dumps(tempos,indent=4))
