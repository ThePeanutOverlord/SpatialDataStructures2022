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
# readCities-opens and reads in the cities.geojson file, writes data out to tempCities.json
# 
# Params:
#   none
#
# Returns:
#   data-all the city data
# ##
def readStates():
  with open("Assignments\P08\states.geojson") as fp:
    data = json.load(fp)
    for state in data:
        state["features"]["properties"]["stroke"] = "#555555"
        state["features"]["properties"]["stroke-width"] = 1
        state["features"]["properties"]["stroke-opacity"] = 1
        state["features"]["properties"]["fill"] = "#8b3737"
        state["features"]["properties"]["fill-opacity"] = ".7"
#   data = data['features']

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
  with open("Assignments\P08\cities.json") as fp:
    data = json.load(fp)

  # for city in data:
  #   city['properties']['distances'] = []

#   writeJsonData(data,"tempCities.json")

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

if __name__=='__main__':
  states = readStates()
  cities = readCities()

