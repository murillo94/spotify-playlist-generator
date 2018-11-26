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


class Search:
    def __init__(self, authenticator, search_value='', search_type='playlist'):
        self.authenticator = authenticator
        self.search_value = search_value
        self.search_type = search_type

    def search(self):
        results = self.authenticator.search(
            q=self.search_type + ':' + self.search_value, type=self.search_type)
        return results


@click.command()
@click.option('--analyze', '-a', help='Insert a playlist name to create new playlist with based songs in inserted playlist', required=True)
def main(analyze):
    cli_id = '30046b20b1d443cf9a9b9175e82b0970'
    cli_sec = '02bdac6c364b4b7091cbd58248473738'

    authenticate = Auth(cli_id, cli_sec).authenticate()
    search = Search(authenticate, analyze, 'playlist').search()
    print(search)
