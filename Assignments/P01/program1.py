import json
import random

with open("Assignments\P01\cities.json") as f:
  data = json.load(f)

def randColor():
  r = lambda: random.randint(0,255)
  return ('#%02X%02X%02X' % (r(),r(),r()))

FeatureCollection = {}
FeatureCollection["type"] = "FeatureCollection"
FeatureCollection["features"] = []

states = {}

for item in data:
    if not item["state"] in states:
      states[item["state"]] = []
    states[item["state"]].append(item) #under the state's name, append the item

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


# for item in states:
#   if not item in grtcty:
#     grtcty[states[item["state"]]] = []
#     grtcty[states[item["state"]]].append(item)

#   elif item["population"] > grtcty[item["state"]]["population"]:
#     grtcty[item["state"]] = item


# for i in data:
#   if not i["state"] in grtcty:
#     grtcty[i["state"]] = []
#     grtcty[i["state"]].append(item)
#   elif int(data[i["population"]]) > int(grtcty[i["state"]["population"]]):
#       grtcty[i["state"]] = data[i]

# for state in states:
#   print(f"{state} = {len(states[state])}") #prints amount of times the state appears in data

points = []

for stateInfo in data:
  points.append(makePoint(stateInfo))

FeatureCollection["features"].append(points)
# points = []
# for info in data:
#   points.append(makePoint(info))

with open("Assignments\P01/new.geojson","w") as f:
  json.dump(FeatureCollection,f,indent=4)

