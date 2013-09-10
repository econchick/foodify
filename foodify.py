# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
import requests as r

app = Flask(__name__)

class FoodifyError(Exception):
    pass


TRACK_SEARCH = "http://ws.spotify.com/search/1/track.json"


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/food/')
def foodify():
    foods = request.args['foods']
    try:
        tracks = grab_tracks(foods)
    except FoodifyError as e:
        error = "Hello, an error! error = %s" % e
        return render_template('error.html', error=error)

    songs = parse_songs(tracks)
    song_data = parse_song_data(tracks)
    return render_template('food.html', foods=songs, song_data=song_data[:10])


def grab_tracks(search_term):
    payload = {"q" : search_term}
    try:
        response = r.get(TRACK_SEARCH, params=payload)
        return response.json()
    except Exception as e:
        raise FoodifyError(e)


def parse_songs(json_response):
    songs = []
    for track in json_response['tracks']:
        # javascript complains if not explicitly encoded in 'utf-8'.
        name = track['name'].encode('utf-8')
        songs.append(name)
    return list(set(songs))


def remove_dup_songs(tracks):
    return [dict(tup) for tup in set(tuple(item.items()) for item in tracks)]


def parse_song_data(json_response):
    tracks = []
    for track in json_response['tracks']:
        song_data = {}
        song_data['album'] = track['album']['name']
        song_data['href'] = track['href']
        song_data['artists'] = track['artists'][0]['name']
        song_data['name'] = track['name']
        tracks.append(song_data)

    tracks = remove_dup_songs(tracks)
    return tracks
