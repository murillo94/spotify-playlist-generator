import random
import click
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# https://github.com/wilddima/vodopad/tree/master/vodopad


class Auth:
    def __init__(self, cli_id='', cli_secret=''):
        self.cli_id = cli_id
        self.cli_secret = cli_secret

    def authenticate(self):
        client_credentials_manager = SpotifyClientCredentials(
            client_id=self.cli_id, client_secret=self.cli_secret)
        sp = spotipy.Spotify(
            client_credentials_manager=client_credentials_manager)
        return sp


class Analyze:
    def __init__(self, authenticator, user_id='', playlist_id='', score=0):
        self.authenticator = authenticator
        self.user_id = user_id
        self.playlist_id = playlist_id
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
        list1 = [('0WOxhx4hikIsyF3CRPLC8W', 79)]
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
                            # add para list_tracks_id, fazer random e depois criar playlist e add na playlist (user_playlist_add_tracks).
        return list_tracks_id

    def analyze(self):
        res = self.authenticator.user_playlist_tracks(
            self.user_id, self.playlist_id, fields='next, items(track(popularity, artists(id)))')
        tracks = res['items']
        while res['next']:
            res = self.authenticator.next(res)
            tracks.extend(res['items'])
        artists = self.get_artist(tracks)
        return self.find_artist_related(artists)


@click.command()
@click.option('--user', '-u', help='Insert a user id', default='12141429536', required=True)
@click.option('--playlist', '-p', help='Insert a playlist id', default='6C9TO1dfZZQTHedI8Qv18p', required=True)
@click.option('--score', '-s', help='Insert a score 0/100 to get assorted artists in playlist', default=100, required=False)
def main(user, playlist, score):
    cli_id = '30046b20b1d443cf9a9b9175e82b0970'
    cli_sec = '02bdac6c364b4b7091cbd58248473738'

    authenticate = Auth(cli_id, cli_sec).authenticate()
    analyze = Analyze(authenticate, user, playlist, score).analyze()
