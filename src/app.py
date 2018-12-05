import sys
import webbrowser

import click
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from tqdm import tqdm


class Auth:
    def __init__(self, user_id=None, cli_id=None, cli_secret=None):
        self.user_id = user_id
        self.cli_id = cli_id
        self.cli_secret = cli_secret

    def authenticate(self):
        scopes = 'playlist-modify-public'
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

    def check_list(func):
        def valid(self, list):
            if len(list) == 0:
                print('Playlist need to have one music at least, please insert another!')
                sys.exit(0)
            return func(self, list)
        return valid

    def get_score(self, length=0):
        if self.score > length:
            return length
        return self.score

    @check_list
    def get_artist_info(self, list=[]):
        results = [(x['track']['artists'][0]['id'], x['track']['id'], x['track']['popularity'])
                   for x in list if 'track' in x]
        length_list = self.get_score(len(results))
        return {'list': results, 'limit': length_list}

    def find_recommendation(self, **kwargs):
        list = kwargs['list'][0:3]
        seed_artists = []
        seed_tracks = []
        for item in tqdm(list, desc="Analyzing music"):
            seed_artists.append(item[0])
            seed_tracks.append(item[1])
        recommendations = self.authenticator.recommendations(
            seed_artists=seed_artists, seed_tracks=seed_tracks[0:2], seed_genres=None, limit=kwargs['limit'])
        recommendations_tracks = [(x['id'], x['popularity'])
                                  for x in recommendations['tracks'] if 'id' in x]
        sort_tracks = sorted(
            recommendations_tracks, key=lambda artist: artist[1], reverse=True)
        tracks = [x[0] for x in sort_tracks]
        return tracks

    def create_playlist(self, tracks=[]):
        playlist_new = self.authenticator.user_playlist_create(
            self.user_id, self.name)
        self.authenticator.user_playlist_replace_tracks(
            self.user_id, playlist_new['id'], tracks)

        if click.confirm('Do you want to open the browser to listen your playlist created?'):
            self.open_browser(playlist_new['external_urls']['spotify'])

    def open_browser(self, url):
        webbrowser.open(url, new=0, autoraise=True)

    def analyze(self):
        res = self.authenticator.user_playlist_tracks(
            self.playlist_user_id, playlist_id=self.playlist_id, fields='next, items(track(popularity, id, artists(id)))')
        tracks = res['items']
        while res['next']:
            res = self.authenticator.next(res)
            tracks.extend(res['items'])
        artists = self.get_artist_info(tracks)
        recommendation = self.find_recommendation(**artists)
        self.create_playlist(recommendation)


@click.command()
@click.option('--user', '-u', help='Insert your spotify user id', required=True)
@click.option('--user-playlist-id', '-upi', help='Insert a spotify user id of playlist owner', required=True)
@click.option('--playlist', '-p', help='Insert a spotify playlist id', required=True)
@click.option('--name', '-n', help='Insert a playlist name', required=True)
@click.option('--score', '-s', help='Insert a score 0/100 to get assorted artists in playlist', default=100, type=click.IntRange(0, 100), required=False)
def main(user, user_playlist_id, playlist, name, score):
    cli_id = '30046b20b1d443cf9a9b9175e82b0970'
    cli_sec = '02bdac6c364b4b7091cbd58248473738'

    print('Authenticating ...')

    authenticate = Auth(user, cli_id, cli_sec).authenticate()
    analyze = Analyze(authenticate, user, user_playlist_id,
                      playlist, name, score).analyze()
