import json
import random

with open("P01\cities.json") as f:
  data = json.load(f)

def randColor():
  r = lambda: random.randint(0,255)
  return ('#%02X%02X%02X' % (r(),r(),r()))


def makePoint(city):
  feature = {
    "type": "Feature",
    "properties": {
      "marker-color":randColor(),
      "marker-symbol": 'A'
    },
    "geometry": {
      "type": "Point",
      "coordinates": [0,0]
    }
  }
  for key,val in city.items():
    if key == 'latitude':
      feature['geometry']['coordinates'][1] = val
    elif key == 'longitude':
      feature['geometry']['coordinates'][0] = val
    else:
      feature['properties'][key] = val

  return feature






points = []
for info in data:
  points.append(makePoint(info))

with open("P01/new.geojson","w") as f:
  json.dump(points,f,indent=4)

