import random as rnd

class Location:
    def __init__(lat = None, lng = None):
        self.lat = lat
        self.lng = lng

    def random():
        self.lat = (rnd.random() * 90) - 90
        self.lng = (rnd.random() * 180) - 180
        return self.coordinates()

    def coordinates():
        return (self.lat, slef.lng)

lat = 48.854171
lng = 2.347479  # Somewhere in Paris
BASE = "http://maps.googleapis.com/maps/api/streetview?sensor=false&"
API  = "AIzaSyAVPqkewX9xOW1RFdUdEWLc4k6zqjipTW4"

URL = "{BASE}size=640x640&key={API}&location=".format(BASE=BASE, API=API)

print("{URL}{LAT},{LNG}".format(URL=URL, LAT=lat, LNG=lng))
