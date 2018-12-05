# Spotify Playlist Generator

Analyze your spotify playlists and create playlist with new songs.

## Overview

A tool for finding playlist and create other playlist with similar music.

### Install

Using pipenv:

```
pipenv install
```

And then execute:

```
pipenv shell
```

### Usage

Arguments:

* `--user`, `-u` - Your spotify user id
* `--user-playlist-id`, `-upi` - Spotify user id of playlist owner
* `--playlist`, `-p` - Spotify playlist id
* `--name`, `-n` - Playlist name to be created
* `--score`, `-s` - Score 0/100 to get assorted artists in playlist

Example:

```
analyze -u tr6amda6xwmpllo403xl9lf9c -upi 12141429536 -p 6C9TO1dfZZQTHedI8Qv18p -n 'Playlist test'
```

### Example

![Example](./resources/example.gif)
