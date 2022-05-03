# Spatial Game API
## Paige Champagne

Using FastApi as a library, write a backend api that can be used to assist your game into becoming a reality.
Create routes that do the following:
Gets a single polygon from the countries geojson data, the polygon that best represents the countries border.
Get a list of country names that could be used to display to a user.
Get a list of country "suggestions" as determined by a partial string match to a key value sent from the user.
Get a point that represents the center of a polygon to help in a distance calculation between countries.
Get the distance between:
Two points
Two polygons (implemented preferably as discussed in class)
Get a hint from the api (returns the "continent" that the goal country resides on (in?)).
Any other routes you may need to help run the game.

### Files

|   #   | Folder Link | Assignment Description |
| :---: | ----------- | ---------------------- |
|  module/\_\_init__.py    |   [__init__.py](module/__init__.py)          | MODULE: init file   |
|   module/features.py    |   [features.py](module/features.py)          | MODULE: contains features, featureCollections classes, methods   |
|   module/helperClasses.py    |   [helpterClasses.py](module/helperClasses.py)          | MODULE: loads countries from file and into spatial index   |
|   module/merger.py    |   [merger.py](module/merger.py)          | MODULE: merges polygons  |
|   api.py    |   [api.py](api.py)          | API code  |
|   countries_stanford.geojson    |   [countries_stanford.geojson](countries_stanford.geojson)          | Big data file  |
|   countries.geojson    |   [countries.geojson](countries.geojson)          | normal data file  |
|   main.py    |   [main.py](main.py)          | I made this when I was first making the API but I don't think I need it anymore  |