# Spatial Game Helper Classes
## Paige Champagne

Have a "backend" nearly completed to service your game.
This doesn't mean it has to be a fully functional "api" but it does need to be a set of classes, organized so that you can do the following:
Get a country polygon
Combine a multi-polygon into a single polygon
Load 1-N country polygons into a spatial index (if geopandas works correctly for distance)
Calculate the distance between two polygons (if geopandas doesn't work correctly)
Reduce the number of points in a polygon
Your class(es) should be in the form of a module.

### Files

|   #   | Folder Link | Assignment Description |
| :---: | ----------- | ---------------------- |
|   Europe.geojson    |   [Europe.geojson](data/Europe.geojson)          | geojson test data file for Europe   |
|   \_\_init__.py    |   [__init__.py](module/__init__.py)          | init file for modules   |
|   features.py    |   [features.py](module/features.py)          | contains features, featureCollections classes, methods   |
|   helperClasses.py    |   [helpterClasses.py](module/helperClasses.py)          | loads countries from file and into spatial index   |
|   merger.py    |   [merger.py](module/merger.py)          | merges polygons  |