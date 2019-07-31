# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 23:28:21 2019

This file contains helper functions that connect to Spotify's API through the
spotipy module and then extract data. It loads all data for all tracks with the
artist, including compilations, rereleases, and guest performances. Spotify has
a 50-album limit per artist, which is reasonable. 

I tried to edit out all the for loops, but it's still quite slow. 



@author: Priyam
"""

username = '1tu40rrjfobuz7luh9rctvb9g'
client_id = '7cf30fc394274566bd5766cb05d66e89'
client_secret = '9d5ffc176b494fdebd24c970832358dd'

album_limit = 50
import spotipy

from spotipy.oauth2 import SpotifyClientCredentials
from kpop_playlist_v2 import twice, blackpink


client_credentials_manager = SpotifyClientCredentials(client_id,client_secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

"""
From each track: name, features
From each album: title, release date, tracklist, track (also available markets)
From each artist: name, followers, popularity, albums
"""
import pandas as pd
import numpy as np



def add_track(track_no):
    """
    Retrieves track features using spotipy.
    
    This helper function retrieves audio features for a given track in an album.
    
    Parameters:
    track_no (int): track number in album
    
    Returns:
    Dataframe row containing features for given track
    
    """
    track_id = track_no['id']
    track_feats = sp.audio_features(track_id)[0]
    title = track_no['name']
    try:
        track_feats.update({'song title':title})
        return track_feats
    except:
        print("no features for " + title)
        return np.nan
 


            
def add_album(album):
    """
    Retrieves audio features for an entire album.
    
    This helper function retrieves audio features for all tracks in a given album.
    
    Parameters:
    album (dataframe): 
    
    Returns:
    Dataframe with audio features as columns and album tracks as rows
    
    """
    
    album_id = album['id']
    tracklist = sp.album_tracks(album_id)['items']
    album_dict = (add_track(track_no) for track_no in tracklist)
    
    album_df = pd.DataFrame(album_dict)
    album_df['album title'] = album['name']
    album_df['album group'] = album['album_group']
    album_df['album type'] = album['album_type']
    album_df['release date'] = album['release_date']    
    
    return (album_df)

def concat_albums(albums):
    """Generate a single dataframe from a list of album dataframes."""
    
    return pd.concat([add_album(album) for album in albums],0)


def artist_update(artist):
    """
    Retrieves audio features from artist discography.
    
    This helper function retrieves audio features from every track on every
    album in an artist's discography. It relies on the above helpers.
    
    Parameters:
    artist (str): name of artist
    
    Returns:
    Dataframe containing features every track by this artist.
    
    """
    artist_albums = sp.artist_albums(artist,limit=album_limit)
    albums = artist_albums['items']
    
    
    artist_library = concat_albums(albums)
    artist_library['artist name']=sp.artist(artist)['name']

    return artist_library


def get_artist_info(artist):
    """
    Retrieves artist information using spotipy.
    
    This helper function retrieves Spotify data for an artist, like their
    popularity, number of followers, and what genres they represent.
    
    Parameters:
    track_no (int): track number in album
    
    Returns:
    Dictionary containing artist name, followers, genres, and popularity.
    
    """
    a_dict = sp.artist(artist)
    artist_info = {'artist name':a_dict['name'],
                  'followers': a_dict['followers']['total'],
                  'genres':[a_dict['genres']],
                  'popularity':a_dict['popularity'],
                  }
    return artist_info

def artists_music(artists):
    """Merges multiple artists' discographies into one large dataframe."""
    
    df = pd.concat([artist_update(artist) for artist in artists],0)
    df = df.reset_index(drop=True).drop(['analysis_url','id','track_href','type','uri'],1)
    return df
    
def artists_info(artists):
    """Merges multiple artists' info into one dataframe."""
    
    artists_info = (get_artist_info(artist) for artist in artists)
    return pd.DataFrame(artists_info)


