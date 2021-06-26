import requests
import urllib.parse
import base64

class SpotifyAPIHandler:
    def __init__(self):
        self.code = ""
        self.bearer = ""
        self.refresh = ""
        self.headers = {"Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.bearer} 

    def authorize(self, code):
        self.code = code

        auth_str = bytes('{}:{}'.format(client_id, client_secret), 'utf-8')
        b64_auth_str = base64.b64encode(auth_str).decode('utf-8')

        headers = {
            "Authorization": "Basic " + b64_auth_str,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "authorization_code",
            "code": self.code,
            "redirect_uri": "https://env32z6nfqh1yfc.m.pipedream.net/callback/",
        }

        response = requests.post("https://accounts.spotify.com/api/token/", data=data, headers=headers)
        print(response.json())
        self.bearer = response.json()["access_token"]
        self.refresh = response.json()["refresh_token"]

        self.headers["Authorization"] = "Bearer " + self.bearer

    def access(self, access):
        self.bearer = access
        self.headers["Authorization"] = "Bearer " + self.bearer

    def request_put(self, url, data):
        print(f"Put requesting {url} with {data}")
        response = requests.put(url, data=data, headers=self.headers)
        print(response.content)
        try:
            return response.json()
        except:
            return ""

    def request_post(self, url):
        print(f"Post requesting {url}")
        response = requests.post(url, headers=self.headers)
        print(response.content)
        try:
            return response.json()
        except:
            return ""

    def request_get(self, url):
        print(f"Get requesting {url}")
        response = requests.get(url, headers=self.headers)
        print(response.content)
        try:
            return response.json()
        except:
            return ""

    def resume(self):
        self.request_put("https://api.spotify.com/v1/me/player/play", "{}")
    
    def pause(self):
        self.request_put("https://api.spotify.com/v1/me/player/pause", "{}")

    def get_info(self):
        self.request_get("https://api.spotify.com/v1/me/player")

    def get_track(self):
        track_data = self.request_get("https://api.spotify.com/v1/me/player/currently-playing?market=US")
        print(track_data["item"]["name"])

    def skip(self):
        self.request_post("https://api.spotify.com/v1/me/player/next")

    def play_album(self, album, position, position_ms=0):
        #spotify:album:5ht7ItJgpBH7W6vJ5BqpPr
        data = '''{
                    "context_uri": "''' + album + '''",
                    "offset": {
                        "position": '''+ str(position) + '''
                    },
                     "position_ms": ''' + str(position_ms) + '''
                }'''
        self.request_put("https://api.spotify.com/v1/me/player/play", data)


    def play_uris(self, uris, position, position_ms=0):
        #spotify:album:5ht7ItJgpBH7W6vJ5BqpPr
        data = '''{
                    "context_uri": "''' + uris + '''",
                    "offset": {
                        "position": '''+ str(position) + '''
                    },
                     "position_ms": ''' + str(position_ms) + '''
                }'''

        self.request_put("https://api.spotify.com/v1/me/player/play", data)


    def play_song(self, song, position_ms=0):
        #spotify:album:5ht7ItJgpBH7W6vJ5BqpPr
        data = '''{
                    "uris": "''' + str([song]) + '''",
                     "position_ms": ''' + str(position_ms) + '''
                }'''
        self.request_put("https://api.spotify.com/v1/me/player/play", data)


    def add_queue(self, song):
        #song = "spotify:track:4iV5W9uYEdYUVa79Axb7Rh"
        self.request_post(f"https://api.spotify.com/v1/me/player/queue?uri={song}")

    def seek(self, ms):
        self.request_put(f"https://api.spotify.com/v1/me/player/seek?position_ms={ms}", "{}")
