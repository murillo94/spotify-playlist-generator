# Spotify Playlist Generator

Analyze your spotify playlists and create playlist with new songs.

## Overview

A tool for finding playlist and create other playlist with similar music.

### Install

Directly from [PyPI](https://pypi.org/project/spotify-playlist-generator/):

```
pip install spotify-playlist-generator
```

You can also install using pipenv:

```
pipenv install
```

And then execute:

```
pipenv shell
```

### Usage

Arguments:

- `--user`, `-u` - Your spotify user id
- `--user-playlist-id`, `-upi` - Spotify user id of playlist owner
- `--playlist-id`, `-pi` - Spotify playlist id
- `--name`, `-n` - Playlist name to be created
- `--diversity`, `-d` - Number 0/100 to get assorted (diversity) artists in playlist

Example:

> You can use `spotify-playlist-generator` ou `spg` to run.

```
spg -u tr6amda6xwmpllo403xl9lf9c -upi 12141429536 -pi 6C9TO1dfZZQTHedI8Qv18p -n 'Playlist test'
```

### Example

![Example](https://github.com/murillo94/spotify-playlist-generator/blob/master/resources/example.gif)
