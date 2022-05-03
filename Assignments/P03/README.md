# Voronoi - Real World Use Case
## Paige Champagne

Create a voronoi diagram over the US creating polygons around each of the 49 cities.
Load said polygons into a spatial tree (geopandas rtree).
Load each of the UFO sighting points into the same rtree.
Query the rtree getting the UFO sighting points that are contained within each polygon.
Save results to a json file to be used later (maybe).

### Files

|   #   | Folder Link | Assignment Description |
| :---: | ----------- | ---------------------- |
|   cities_small.geojson    |   [cities_small.geojson](data/cities_small.geojson)          | geojson data file for cities   |
|   ufo_data.geojson    |   [ufo_data.geojson](data/ufo_data.geojson)          | geojson file for ufo data   |
|   us_nation_border.geojson    |   [us.nation_border.geojson](data/us.nation_border.geojson)          | data for the U.S. border   |
|   00_PointsPoly.jpg    |   [00_PointsPoly.jpg](00_PointsPoly.jpg)          | every UFO sighting displayed on the map   |
|   00_voronoi.jpg    |   [00_voronoi.jpg ](00_voronoi.jpg )          | Voronoi diagram of the U.S.   |
|   ufos_in_Polys.json    |   [ufos_in_Polys.json ](ufos_in_Polys.json )          |  Output file of all the UFO points for each polygon in the above voronoi diagram  |