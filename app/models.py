# -*- coding: utf-8 -*-

import requests as r


class FoodifyError(Exception):
    pass


TRACK_SEARCH = "http://ws.spotify.com/search/1/track.json"


def grab_tracks(search_term):
    payload = {"q" : search_term}
    try:
        response = r.get(TRACK_SEARCH, params=payload)
        return response.json()
    except Exception, e:
        raise FoodifyError(e)

def parse_songs(json_response):
    songs = []
    for track in json_response['tracks']:
        name = track['name'].encode('utf-8', "ignore")
        songs.append(name)
    return list(set(songs))


def parse_song_data(json_response):
    tracks = []
    for track in json_response['tracks']:
        song_data = {}
        song_data['album'] = track['album']['name'].encode('utf-8')
        song_data['popularity'] = track['popularity'].encode('utf-8', "ignore")
        song_data['href'] = track['href'].encode('utf-8', "ignore")
        song_data['artists'] = track['artists'][0]['name'].encode('utf-8', "ignore")
        song_data['name'] = track['name'].encode('utf-8', "ignore")
        tracks.append(song_data)
    return tracks