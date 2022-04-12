####
#
# Author: Paige Champagne
# Label: Program 2
# Title: Rtree Nearest Neighbor with UFO's
# Course: CMPS 4553
# Semester: Spring 2022
#
# Description: Reads in a ufo csv file and a cities geojson.
#               -creates a ufo geodataframe
#               -finds distance from each city to others and puts in temp file
#               -finds avg nearest 100 ufo distances from each city and puts in json file
#
# Files:
#   input:  cities.geojson -cities input file
#           ufo_data.csv   -ufo input file
#   code:   program2.py    -driver code
#   output: Cities.json    -final output file with closest 100 avg ufo distances
#           tempCities.json-midpoint output file converting it from geojson to json
#           tempDistances.json-output file with distances from each cities to the others
#       
####

import json
import numpy as np
import pandas as pd
import geopandas
from shapely.geometry import box, Polygon, LineString, Point
from rich import print
import math

import os
import sys

##
# haversineDistance-finds haversine distance between two points given the
#   longitude and latiude values of those points
# 
# Params:
#   lon1-first longitude value
#   lat1-first latitude value
#   lon2-second longitude value
#   lat2-second latitude value
#   units-the unit of measurement it will be in (automatically miles)
#
# Returns:
#   the haversine distance between (lon1,lat1) and (lon2,lat2)
# ##
def haversineDistance(lon1, lat1, lon2, lat2, units="miles"):
    """Calculate the great circle distance in kilometers between two points on the earth (start and end) where each point
        is specified in decimal degrees.
    Params:
        lon1  (float)  : decimel degrees longitude of start (x value)
        lat1  (float)  : decimel degrees latitude of start (y value)
        lon2  (float)  : decimel degrees longitude of end (x value)
        lat3  (float)  : decimel degrees latitude of end (y value)
        units (string) : miles or km depending on what you want the answer to be in
    Returns:
        distance (float) : distance in whichever units chosen
    """
    radius = {"km": 6371, "miles": 3956}

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    r = radius[units]  # choose miles or km for results
    return c * r

##
# readCities-opens and reads in the cities.geojson file, writes data out to tempCities.json
# 
# Params:
#   none
#
# Returns:
#   data-all the city data
# ##
def readCities():
  with open("cities.geojson") as fp:
    data = json.load(fp)

  data = data['features']

  # for city in data:
  #   city['properties']['distances'] = []

  writeJsonData(data,"tempCities.json")

  return data

##
# calcDistances-calculates distances from each city to the others, prints to file
# 
# Params:
#   data-all the city data
#
# Returns:
#   data-revised city data with distances property
# ##
def calcDistances(data):
  for i in range(len(data)):
    lon1,lat1 = data[i]['geometry']['coordinates']
    for j in range(len(data)):
      lon2,lat2 = data[j]['geometry']['coordinates']
      data[i]['properties']['distances'].append(haversineDistance(lon1, lat1, lon2, lat2))

  writeJsonData(data,"tempDistances.json")
  return data

##
# writeJsonData-writes json data to the file
# 
# Params:
#   data-data to be written
#   filename-file to be written to
#
# Returns:
#   none
# ##
def writeJsonData(data,filename):
  with open(filename,"w") as fp:
    json.dump(data,fp,indent=2)

##
# loadUfos-loads in ufo csv file and creats geodataframe
# 
# Params:
#   none
#
# Returns:
#   gdf-ufo geodataframe
# ##
def loadUfos():

  df = pd.read_csv("ufo_data.csv")
  
  #print(df.head())

  gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.lon, df.lat))
  #gdf.set_crs(epsg=4326, inplace=True)
  #print(gdf.head())
  return gdf


##
# findClosestUfos-finds the closest 100 ufo sightings and averages them and assigns
#       that value to the city
# 
# Params:
#   data-cities data
#   gdf-ufo geodataframe
#
# Returns:
#   none
# ##
def findClosestUfos(data,gdf):

  # make a geoseries using the ufo data frame's geometry field
  s = geopandas.GeoSeries(gdf['geometry'])
  #s.set_crs(epsg=4326)

  # loop through each city
  for city in data:
    print(f"{city['properties']['city']} {city['properties']['state']}")
    # get the coords for that city
    lon,lat = city['geometry']['coordinates']
    
    # get the distance from that city to EVERY ufo
    distances = []
    for u in s:
      # print(u.y)
      distances.append(haversineDistance(lon, lat, u.x, u.y))
      
    distances.sort()
    sum = 0
    for i in range(100):
      sum += distances[i]

    avg = sum/100

    city["properties"]["Average-UFO-Distance"] = avg
    
if __name__=='__main__':
  data = readCities()
  # data = calcDistances(data)
  gdf = loadUfos()
  findClosestUfos(data,gdf)
  writeJsonData(data,"Cities.json")