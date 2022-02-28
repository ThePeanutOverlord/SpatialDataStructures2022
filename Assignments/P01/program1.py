import json
import random

with open("Assignments\P01\cities.json") as f:
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

states = {}
for item in data:
    if not item["state"] in states:
      states[item["state"]] = []
    states[item["state"]].append(item)


greatstate = {}

for city in states:
  for c in states[city["state"]]:
    if not c["population"] in greatstate:
      greatstate[c["population"]] = []
      greatstate[c["population"]].append(c)
    elif int(c["population"]) > int(greatstate[c["population"]]):
      greatstate[c["population"]] = c["population"]



# for city in states:
#   if not states[city] in greatstate:
#       greatstate[states[city]] = []
#   elif states[city["population"]] > greatstate[states]:
#       greatstate[states[city]] = states[city]
  # print(f"{state} = {len(states[state])}") #prints amount of times the state appears in data

points = []

for stateInfo in data:
  points.append(makePoint(stateInfo))

# points = []
# for info in data:
#   points.append(makePoint(info))

with open("Assignments\P01/new2.geojson","w") as f:
  json.dump(points,f,indent=4)

