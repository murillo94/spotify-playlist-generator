import random

import click
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials


class Auth:
    def __init__(self, user_id=None, cli_id=None, cli_secret=None):
        self.user_id = user_id
        self.cli_id = cli_id
        self.cli_secret = cli_secret

    def authenticate(self):
        scopes = 'playlist-modify-public playlist-read-collaborative'
        token = util.prompt_for_user_token(
            self.user_id, scope=scopes, client_id=self.cli_id, client_secret=self.cli_secret, redirect_uri='http://localhost:8888/callback/')

        if token:
            sp = spotipy.Spotify(auth=token)
            sp.trace = False
            return sp


class Analyze:
    def __init__(self, authenticator, user_id='', playlist_user_id='', playlist_id='',  name='', score=0):
        self.authenticator = authenticator
        self.user_id = user_id
        self.playlist_user_id = playlist_user_id
        self.playlist_id = playlist_id
        self.name = name
        self.score = score

    def get_artist(self, list=[]):
        results = [(x['track']['artists'][0]['id'], x['track']['popularity'])
                   for x in list if 'track' in x]
        sort = sorted(results, key=lambda artist: artist[1], reverse=True)
        length_list = self.get_score(len(sort))
        rand = random.sample(sort, length_list)
        return rand

    def get_score(self, length=0):
        if self.score > length:
            return length
        return self.score

    def find_artist_related(self, list=[]):
        list_tracks_id = []
        list1 = [('0epOFNiUfyON9EYx7Tpr6V', 79)]
        for item in list1:
            if item[0]:
                artist = self.authenticator.artist_related_artists(item[0])
                artist_infos = artist['artists'][0]
                if artist_infos:
                    for info, value in artist_infos.items():
                        if info == 'id':
                            tracks = self.authenticator.artist_top_tracks(
                                value)
                            tracks_list = tracks['tracks'][0:1]
                            list_tracks_id.append(
                                tracks_list[0]['album']['id'])
        list_tracks_id_shuffle = random.sample(
            list_tracks_id, len(list_tracks_id))
        return list_tracks_id_shuffle

    def create_playlist(self):
        playlist = self.authenticator.user_playlist_create(
            self.user_id, self.name)
        return playlist['id']

    def analyze(self):
        res = self.authenticator.user_playlist_tracks(
            self.playlist_user_id, self.playlist_id, fields='next, items(track(popularity, artists(id)))')
        tracks = res['items']
        while res['next']:
            res = self.authenticator.next(res)
            tracks.extend(res['items'])
        artists = self.get_artist(tracks)
        return self.find_artist_related(artists)


@click.command()
@click.option('--user', '-u', help='Insert your user id', required=True)
@click.option('--user-playlist-id', '-upi', help='Insert a user id of playlist owner', required=True)
@click.option('--playlist', '-p', help='Insert a playlist id', required=True)
@click.option('--name', '-n', help='Insert a playlist name', required=True)
@click.option('--score', '-s', help='Insert a score 0/100 to get assorted artists in playlist', default=100, required=False)
def main(user, user_playlist_id, playlist, name, score):
    cli_id = '30046b20b1d443cf9a9b9175e82b0970'
    cli_sec = '02bdac6c364b4b7091cbd58248473738'

    authenticate = Auth(user, cli_id, cli_sec).authenticate()
    analyze = Analyze(authenticate, user, user_playlist_id,
                      playlist, name, score).analyze()

# analyze -u tr6amda6xwmpllo403xl9lf9c -upi 12141429536 -p 6C9TO1dfZZQTHedI8Qv18p -n testando
