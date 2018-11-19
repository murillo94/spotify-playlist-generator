import argparse
import spotipy

#https://spotipy.readthedocs.io/en/latest/#client-credentials-flow
#https://github.com/plamere/spotipy/issues/194

parser = argparse.ArgumentParser(description="Analyze your spotify playlists songs and create playlist with new songs.")

parser.add_argument("--artist", dest="artist", default="", help="Search a artist", required=False)
parser.add_argument("--playlist", dest="playlist", default="", help="Search a playlist", required=False)
parser.add_argument("--analyze", dest="analyze", default="", help="TODO", required=False)

args = parser.parse_args()

spotify = spotipy.Spotify()
results = spotify.search(q='artist:' + args.artist, type='artist')

print(results)
print(args.artist)