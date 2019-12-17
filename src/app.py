import sys
import webbrowser
import click
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from tqdm import tqdm

URL_CALLBACK = 'http://localhost:8888/callback/'


class Service:
    def __init__(self, user_id=None, cli_id=None, cli_secret=None):
        self.user_id = user_id
        self.cli_id = cli_id
        self.cli_secret = cli_secret

    def get_spotify_service(self):
        scopes = 'playlist-modify-public'
        token = util.prompt_for_user_token(
            self.user_id, scope=scopes, client_id=self.cli_id, client_secret=self.cli_secret, redirect_uri=URL_CALLBACK)

        if token:
            service = spotipy.Spotify(auth=token)
            service.trace = False
            return service


class Analyze:
    def __init__(self, service, user_id='', playlist_user_id='', playlist_id='',  name='', diversity=0):
        self.service = service
        self.user_id = user_id
        self.playlist_user_id = playlist_user_id
        self.playlist_id = playlist_id
        self.name = name
        self.diversity = diversity

    def check_list(func):
        def valid(self, list):
            if len(list) == 0:
                print('Playlist need to have one music at least, please insert another!')
                sys.exit(0)
            return func(self, list)
        return valid

    def _open_browser(self, url):
        webbrowser.open(url, new=0, autoraise=True)

    def _get_diversity(self, length=0):
        if self.diversity > length:
            return length
        return self.diversity

    @check_list
    def _get_tracks_info(self, list=[]):
        tracks = [(x['track']['artists'][0]['id'], x['track']['id'], x['track']['popularity'])
                  for x in list if 'track' in x]
        limit = self._get_diversity(len(tracks))
        return {'list': tracks, 'limit': limit}

    def _find_recommendations(self, **kwargs):
        list = kwargs['list'][0:3]
        seed_artists = []
        seed_tracks = []
        for item in tqdm(list, desc="Analyzing music"):
            seed_artists.append(item[0])
            seed_tracks.append(item[1])
        recommendations = self.service.recommendations(
            seed_artists=seed_artists, seed_tracks=seed_tracks[0:2], seed_genres=None, limit=kwargs['limit'])
        recommendations_tracks = [(x['id'], x['popularity'])
                                  for x in recommendations['tracks'] if 'id' in x]
        sort_tracks = sorted(
            recommendations_tracks, key=lambda artist: artist[1], reverse=True)
        tracks = [x[0] for x in sort_tracks]
        return tracks

    def _create_playlist(self, tracks=[]):
        playlist_new = self.service.user_playlist_create(
            self.user_id, self.name)
        self.service.user_playlist_replace_tracks(
            self.user_id, playlist_new['id'], tracks)

        if click.confirm('Do you want to open the browser to listen your playlist created?'):
            self._open_browser(playlist_new['external_urls']['spotify'])

    def analyze(self):
        playlist_tracks = self.service.user_playlist_tracks(
            self.playlist_user_id, playlist_id=self.playlist_id, fields='next, items(track(popularity, id, artists(id)))')
        tracks = playlist_tracks['items']
        while playlist_tracks['next']:
            playlist_tracks = self.service.next(playlist_tracks)
            tracks.extend(playlist_tracks['items'])
        tracks_info = self._get_tracks_info(tracks)
        recommendations = self._find_recommendations(**tracks_info)
        self._create_playlist(recommendations)


@click.command()
@click.option('--user', '-u', help='Insert your spotify user id', required=True)
@click.option('--user-playlist-id', '-upi', help='Insert a spotify user id of playlist owner', required=True)
@click.option('--playlist', '-p', help='Insert a spotify playlist id', required=True)
@click.option('--name', '-n', help='Insert a playlist name', required=True)
@click.option('--diversity', '-d', help='Insert a number 0/100 to get assorted (diversity) artists in playlist', default=100, type=click.IntRange(0, 100), required=False)
def main(user, user_playlist_id, playlist, name, diversity):
    cli_id = '30046b20b1d443cf9a9b9175e82b0970'
    cli_sec = '02bdac6c364b4b7091cbd58248473738'

    print('Authenticating...')
    service = Service(user, cli_id, cli_sec).get_spotify_service()

    print('Creating...')
    Analyze(service, user, user_playlist_id,
            playlist, name, diversity).analyze()
