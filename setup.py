from setuptools import setup

setup(name='spotify-playlist-generator',
      description='Analyze your spotify playlists songs and create playlist with new songs',
      entry_points={
          'console_scripts': [
              'analyze = src.__main__:main'
          ]
      },
      )
