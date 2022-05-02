####
#
# Author: Paige Champagne
# Label: Program 3
# Title: Voronoi - Real World Use Case
# Course: CMPS 4553
# Semester: Spring 2022
#
# Description: Create a voronoi diagram over the US creating polygons around each of the 49 cities.
#               Load said polygons into a spatial tree (geopandas rtree).
#               Load each of the UFO sighting points into the same rtree.
#               Query the rtree getting the UFO sighting points that are contained within each polygon.
#               Save results to a json file to be used later (maybe).
#
# Files:
#   input:  cities_small.geojson -cities input file
#           ufo_data.geojson   -ufo input file
#           us_nation_border.geojson    -data for the U.S. border
#   code:   program3.py    -driver code
#   output: 00_PointsPoly.jpg     -every UFO sighting displayed on the map 
#           00_voronoi.jpg -Voronoi diagram of the U.S.
#           ufos_in_Polys.json  -Output file of all the UFO points for each polygon in the above voronoi diagram
#       
####
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import pyproj
import random
import shapely.geometry
import sys
import json
import fiona
fiona.supported_drivers  

from geovoronoi import voronoi_regions_from_coords, points_to_coords
from geovoronoi.plotting import subplot_for_map, plot_voronoi_polys_with_points_in_area
from shapely.ops import unary_union

# from shapely.geometry import box, Polygon, LineString, Point
from shapely.ops import transform

debug = True
spatIndex = None


def loadGeoDataFrame(file, printHead=False):
    """Load a geojson file into a geoDataFrame
    Params:
        file (string)       : path / filename to be loaded
        printHead (bool)    : if True it prints the "head" of the dataframe
    Returns:
        GeoDataFrame re-projected to epsg:3395
    """
    gdf = gpd.read_file(file)
    gdf = gdf.to_crs("EPSG:3395")

    if printHead or debug:
        print(file)
        print(gdf.head(2))

    return gdf


def makeGeoDataFrame(data):
    """makes a geoDataFrame from some coordinate data and re-projects to 3395
    Params:
        data (dict) : dictionary with a "Coordinates" field that has a list of point data
    Returns:
        geoDataFrame projected with "EPSG:3395"
    """
    df = pd.DataFrame(data)
    gdf = gpd.GeoDataFrame(df, geometry="Coordinates", crs="EPSG:3395")

    return gdf


def getBoundingBox(points):
    """Get extremes from a geoDataFrame
    Params:
        points (geoDataFrame) : some geoDataFrame
    Returns:
        tuple : (minx, miny, maxx, maxy)
    """
    # gets extreme bounds (but we dont use it its just to log to console)
    minx, miny, maxx, maxy = points.total_bounds
    return (minx, miny, maxx, maxy)


def plotBorderAndPoints(border, points, saveName=None):
    """Given some outline shape (thats a geoDataFrame) and some points, make a plot to show.
       It doesn't really matter if ones a border and the other is points, basically given
       two geoDataFrames, it will plot them.
    Params:
        border (GeoDataFrame) : GeoDataFrame of the border
        points (GeoDataFrame) : GeoDataFrame of the points
        saveName (string)     : name/path if you want to save plot to a file
    Returns:
        None
    """
    print("plotting" )
    fig, ax = plt.subplots(figsize=(8, 6))
    border.plot(ax=ax, color="gray")
    points.plot(ax=ax, markersize=2, color="blue")

    plt.axis("off")

    if saveName:
        plt.savefig(saveName, bbox_inches="tight")
    # plt.show()


def createVoronoi(boundary, cities):
    """process the boundary (polygon border) and points to create the voronoi diagram.
    Params:
        boundary (geoDataFrame)   : the polygon representing the container of the diagram
        cities   (geoDataFrame)   : the points that represent the "seeds" for the diagram
    Returns:
        All the datastructures needed to plot the voronoi diagram. Most important for us however,
        is the "regionPolys" needed for us to determine which ufos are each of the polygons.

        cityCoords    -  the seeds converted to proper coordinate system for the diagram
        boundaryShape -  the boundary simplified or converted to a single outer ring polygon
        regionPolys   -  a dict of the internal polygons created around each seed
        regionPoints  -  a dict of the points used in the creation of the polygon
    """
    # pre-process data so it works with voronoi
    boundaryProj = boundary.to_crs(epsg=3395)
    citiesProj = cities.to_crs(boundaryProj.crs)
    boundaryShape = unary_union(boundaryProj.geometry)
    cityCoords = points_to_coords(citiesProj.geometry)

    # create the polygons and such
    regionPolys, regionPoints = voronoi_regions_from_coords(cityCoords, boundaryShape)

    # return all the things created so we can use / plot
    return cityCoords, boundaryShape, regionPolys, regionPoints


def plotVoronoi(cityCoords, boundaryShape, regionPolys, regionPoints, saveName=None):
    """plot the voronoi diagram.
    Params:
        cityCoords  (numpy ndarray)     : the seeds converted to proper coordinate system for the diagram
        boundaryShape (shapely polygon) : the boundary simplified or converted to a single outer ring polygon
        regionPolys   (dict)            : a dict of the internal polygons created around each seed
        regionPoints  (dict)            : a dict of the points used in the creation of the polygon
        saveName (string)               : path / filename to save file for plot if wanted
    """

    fig, ax = subplot_for_map(figsize=(8, 6))
    plot_voronoi_polys_with_points_in_area(
        ax, boundaryShape, regionPolys, cityCoords, regionPoints
    )
    if saveName:
        plt.savefig(saveName, bbox_inches="tight")
    # plt.show()


def insertSpatIndex(gdf, epsg=None):
    """Insert some geo shape into the spatial index
    Params:
        gdf (geoDataFrame) : some geo data
        epsg (int)         : some new epsg (like 3395 or 4326) if you want to change the crs
    Returns:
        None
    """
    global spatIndex

    if epsg:
        gdf.to_crs(epsg=epsg)

    if not spatIndex:
        spatIndex = gpd.GeoSeries(gdf["geometry"])
    else:
        spatIndex.append(gdf["geometry"])


def getPolygonUfos(ufos, poly):
    """Query the spatial index given the polygon passed in.
    Params:
        ufos (geoDataFrame)    : data frame of ufos so we use the indexes returned
                                 by query to access the ufo data
        poly (shapely polygon) : the polygon to query with
    Returns:
        results (list) : list if indexes of the points found within the polygon
    """
    global spatIndex  # explicitly says use this global

    indexes = []  # list for resulting indexes found
    coordinates = []  # ufo data using the index from the geoDataFrame

    # This runs the query looking for ufo's that are "within" the polygon
    results = spatIndex.within(poly)

    # if a result in the results list is true, append that index to the results list
    for i in range(len(results)):
        if results[i]:
            indexes.append(i)
            coordinates.append(ufos["geometry"][i])

    # return results in a dataframe ready dictionary
    return {"indexes": indexes, "Coordinates": coordinates}


def reProject(geostructure, src="3395", dest="4326"):
    """Transfrom (change projection) of some shapely shape. Used for shapes and not whole dataFrames
       since the `to_crs()` method is for geoDataFrames.
    Params:
        geoStructure (geoDataFrame) : some geo dataframe to be re-projected
        src (int/string)            : the source projection (what it is)
        dest (int/string)           : the destination projection (what it needs to be)
    Returns:
        list of new coords
    """
    projection = pyproj.Transformer.from_proj(
        pyproj.Proj(init=f"epsg:{src}"),  # source coordinate system
        pyproj.Proj(init=f"epsg:{dest}"),  # destination coordinate system
    )

    reProjected = transform(projection.transform, geostructure)  # apply projection

    return reProjected


def getPolyCoords(poly):
    """Takes a shapely polygon and returns its xy coords making up the polygon.
    I used this to "check" my sanity when comparing different projections
    Params:
        poly (shapely polygon) : not a multipolygon, just a polygon
    Returns:
        returns to lists: one with x coords and one with y coords
    """
    # Extract the point values that define the perimeter of the polygon
    x, y = poly.exterior.coords.xy

    return x, y


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
if __name__ == "__main__":

    # load the geojson files into geoDataFrames with projection 3395
    cities = loadGeoDataFrame("data/cities_small.geojson")
    ufos = loadGeoDataFrame("data/ufo_data.geojson")
    usBorder = loadGeoDataFrame("data/us_nation_border.geojson")

    if debug:
        plotBorderAndPoints(usBorder, cities)
        print("done plotting")
        plotBorderAndPoints(usBorder, ufos)

    # create voronoi diagram. The function returns 4 things!
    cityCoords, boundaryShape, regionPolys, regionPoints = createVoronoi(
        usBorder, cities
    )


    # This function creates the spatial index by inserting the ufo
    # geoDataFrame into the spatIndex (keeping with the projection epsg:3395)
    insertSpatIndex(ufos)

    # stores the data to be put in json
    ufosinPolys = {
      "Polys" : []
    }
    #cycle through the polygons to get each one
    for i in range(len(regionPolys)):
        # make a dataframe for each polygon with the ufos inside it
      temp = makeGeoDataFrame(getPolygonUfos(ufos, regionPolys[i]))
        # append the coordinates of the ufo sightings to the list
      ufosinPolys["Polys"].append([str(temp["Coordinates"])])
  
    # Now plot the voronoi diagram
    plotVoronoi(cityCoords, boundaryShape, regionPolys, regionPoints, "00_voronoi.jpg")

    # and plot the ufos
    plotBorderAndPoints(usBorder, ufos, "00_PointsPoly.jpg")
    #write to file
    writeJsonData(ufosinPolys, "ufos_in_Polys.json")
    # print(ufosinPolys)
