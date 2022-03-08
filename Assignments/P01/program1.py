import json
import random

with open("Assignments\P01\cities.json") as f:
  data = json.load(f)

# def randColor():
#   r = lambda: random.randint(0,255)
#   return ('#%02X%02X%02X' % (r(),r(),r()))

FeatureCollection = {}
FeatureCollection["type"] = "FeatureCollection"
FeatureCollection["features"] = []

states = {}

# for item in data:
#     if not item["state"] in states:
#       states[item["state"]] = []
#     states[item["state"]].append(item) #under the state's name, append the item

for item in data:
    if not item["state"] in states: #fuck it we're just going with one city from each state
      states[item["state"]] = item

    
      # states[item["state"]].append(item) #under the state's name, append the item
    # elif item["state"] in states:
    #   if int(item["population"]) > int(states[item["state"]["population"]]):
    #     states[item["state"]] = item

def makePoint(city):
  feature = {
    "type": "Feature",
    "properties": {
      "marker-color":"#E23C71",
      "marker-symbol": 1,
      "marker-size": "medium"
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

def makeLineString(point1, point2):
  feature = {
    "type": "Feature",
    "properties": {
      "marker-color":"#E23C71",
      "marker-symbol": 1,
      "marker-size": "medium"
    },
    "geometry": {
      "type": "LineString",
      "coordinates": [
        point1,
        point2
      ]
    }
  }
  return feature

# for state in states:
#   print(f"{state} = {len(states[state])}") #prints amount of times the state appears in data

points = []

for stateInfo in data:
  points.append(makePoint(stateInfo))

FeatureCollection["features"].append(points)
# points = []
# for info in data:
#   points.append(makePoint(info))
# print(points['geometry']['coordinates'][0])
lineStrings = []

for i in range(len(points)):
    if i < len(points)-1:
     lineStrings.append(makeLineString(points[i]["geometry"]["coordinates"],points[i+1]["geometry"]["coordinates"]))

FeatureCollection["features"].append(lineStrings)


with open("Assignments\P01/new.geojson","w") as f:
  json.dump(FeatureCollection,f,indent=4)

