import random as rnd
import requests

class Location:
    def __init__(self, lat = None, lng = None):
        self.lat = lat
        self.lng = lng

    def random(self):
        self.lat = (rnd.random() * 90) - 90
        self.lng = (rnd.random() * 180) - 180
        return self.coordinates()

    def coordinates(self):
        return (self.lat, self.lng)

lat = 48.854171
lng = 2.347479  # Somewhere in Paris
BASE = "http://maps.googleapis.com/maps/api/streetview?sensor=false&"
API  = "AIzaSyAVPqkewX9xOW1RFdUdEWLc4k6zqjipTW4"
URL = "{BASE}size=640x640&location={{LAT}},{{LNG}}&key={API}".format(BASE=BASE, API=API)
NEARBY = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"

json_url = None
found = False
lat = lng = 0.0
radius = 20000
location = Location()
attempts = 0

while True:
    attempts += 1
    location.random()
    lat, lng = location.coordinates()

    json_url  = "https://maps.googleapis.com/maps/api/streetview/metadata?location={LAT},{LNG}&key={API}"
    
    nearby_url = "{base}key={api}&location={lat},{lng}&radius={radius}".format(
        base=NEARBY,
        api=API,
        lat=lat, lng=lng,
        radius=radius
    )
    request = requests.get(nearby_url)
    json = request.json()
    status = json.get('status')

    meta = requests.get(json_url).json()

    print(nearby_url)
    print(json)

    if 'ZERO' not in status and 'ZERO' not in meta.get('status'):
        for result in json.get('results'):
            lat = float(result.get('geometry').get('location').get('lat'))
            lng = float(result.get('geometry').get('location').get('lng'))

            meta = requests.get(json_url.format(LAT=lat, LNG=lng, API=API)).json()
            print("Found, looking for street views:\n")
            print(meta)
            if 'ZERO' not in meta.get('status'):
                found = True
                name = "{}".format(result)
                print(name)
                break
    if found: break


final_url = URL.format(LAT=lat, LNG=lng)
print("Found valid coord:", lat, lng)
print("Image URL:        ", final_url)
print("JSON URL:         ", json_url)



