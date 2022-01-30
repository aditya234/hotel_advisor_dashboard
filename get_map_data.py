# importing the requests library
import requests


class GetMapData:
    def __init__(self):
        self.url = "https://api.geoapify.com/v1/geocode/search"
        self.apikey = "2466ca113779425f98d63a81eee49824"

    def get_location(self, location):
        PARAMS = {'text': location, "apiKey": self.apikey}
        try:
            response = requests.get(url=self.url, params=PARAMS)

            if response.status_code == 200:
                data = response.json()
                if len(data['features']) > 0 and 'geometry' in data['features'][0] and 'coordinates' in \
                        data['features'][0][
                            'geometry']:
                    return data['features'][0]['geometry']['coordinates']

            return None
        except:
            return None
