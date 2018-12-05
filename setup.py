from codecs import open
from setuptools import setup

with open('README.md', 'r', 'utf-8') as f:
    readme = f.read()

setup(
    name='spotify-playlist-generator',
    version='0.0.1',
    packages=["src"],
    description='Analyze your spotify playlists songs and create playlist with new songs',
    url="https://github.com/murillo94/spotify-playlist-generator",
    author="Murillo de Miranda Pereira",
    author_email="murillomir0@gmail.com",
    keywords="spotify playlist generator",
    long_description=readme,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'analyze = src.__main__:main'
        ]
    },
    install_requires=[
        'spotipy',
        'click',
        'tqdm'
    ],
    license='MIT'
)
