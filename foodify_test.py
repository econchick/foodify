import flask
import foodify
import mock
import unittest

class FoodifyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = foodify.app
        self.food = 'potatoes'
        self.track_search = "http://ws.spotify.com/search/1/track.json"
        self.json_response = {
            "info": {
                "num_results": 2812,
                "limit": 100,
                "offset": 0,
                "query": "foo",
                "type": "track",
                "page": 1
            },
            "tracks": [{
                "album":{
                    "released": "2009",
                    "href": "spotify:album:1zCNrbPpz5OLSr6mSpPdKm",
                    "name": "Greatest Hits",
                    "availability": {
                        "territories": "AD AT AU BE CA CH DE DK EE ES FI FR GB HK IE IS IT LI LT LU LV MC MX MY NL NO NZ PL PT SE SG US"
                        }
                    },
                "name": "Everlong",
                "popularity": "0.73",
                "external-ids": [{
                    "type": "isrc",
                    "id": "USRW29600011"
                    }],
                "length": 250.259,
                "href": "spotify:track:07q6QTQXyPRCf7GbLakRPr",
                "artists": [{
                    "href": "spotify:artist:7jy3rLJdDQY21OgRLCZ9sD",
                    "name": "Foo Fighters"
                    }],
                "track-number": "3"
                }]
            }

    def test_context(self):
        with self.app.test_request_context('/foods/?foods=pickles'):
            assert flask.request.path == '/foods/'
            assert flask.request.args['foods'] == 'pickles'
            assert flask.request.args['foods'] != 'watermelon'

    def test_grab_tracks(self):
        with mock.patch('requests.get') as patched_get:
            foodify.grab_tracks(self.food)
            patched_get.assert_called_once_with(self.track_search,
                                                params={'q': self.food})

    def test_parse_song(self):
        songs = foodify.parse_songs(self.json_response)
        assert 'Everlong' in songs

    def test_remove_dup_songs(self):
        track = [{'album': 'grape'}, {'album': 'grape'}, {'album': 'peach'}]
        results = foodify.remove_dup_songs(track)
        assert len(results) == 2

    def test_parse_song_data(self):
        tracks = foodify.parse_song_data(self.json_response)
        assert tracks[0]['album'] == "Greatest Hits"
        assert tracks[0]['href'] == "spotify:track:07q6QTQXyPRCf7GbLakRPr"
        assert tracks[0]['artists'] == "Foo Fighters"
        assert tracks[0]['name'] == "Everlong"


if __name__ == '__main__':
    unittest.main()