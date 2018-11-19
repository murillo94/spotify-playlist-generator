import argparse
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

parser = argparse.ArgumentParser(
    description="Analyze your spotify playlists songs and create playlist with new songs.")

parser.add_argument("--artist", dest="artist", default="",
                    help="Search a artist", required=False)
parser.add_argument("--playlist", dest="playlist", default="",
                    help="Search a playlist", required=False)
parser.add_argument("--analyze", dest="analyze",
                    default="", help="Insert a playlist name to create new playlist with based songs in inserted playlist", required=False)

args = parser.parse_args()


class Auth:
    def __init__(self, cli_id, cli_secret):
        self.cli_id = cli_id
        self.cli_secret = cli_secret

    def authenticate(self):
        client_credentials_manager = SpotifyClientCredentials(
            client_id=self.cli_id, client_secret=self.cli_secret)
        sp = spotipy.Spotify(
            client_credentials_manager=client_credentials_manager)
        return sp


class Search:
    def __init__(self, search_value):
        self.search_value = search_value

    def search(self):
        results = authenticate.search(
            q='artist:' + self.search_value, type='artist')
        return results


cli_id = '30046b20b1d443cf9a9b9175e82b0970'
cli_sec = '02bdac6c364b4b7091cbd58248473738'

authenticate = Auth(cli_id, cli_sec).authenticate()
search = Search(args.artist).search()

if __name__ == '__main__':
    if not (args.artist or args.playlist or args.analyze):
        parser.error(
            'No action requested, add --artist or --playlist or --analyze')
    else:
        print(search)
        print(args)
