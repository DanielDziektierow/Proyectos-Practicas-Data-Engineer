import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import pandas as pd 
import numpy as np

import plotly.express as px

from config import client_secret, client_id

client_credentials_manager= SpotifyClientCredentials(client_id= client_id, client_secret= client_secret)
sp= spotipy.Spotify(client_credentials_manager= client_credentials_manager)

#Ejemplo de extraccion de id.

results= sp.search(q= 'David Guetta', limit=1, type='artist')
artist_id= results['artists']['items'][0]['id']
print(artist_id)

albums= sp.artist_albums(artist_id, album_type= 'album' )
for album in albums['items']:
    print(album['name'])