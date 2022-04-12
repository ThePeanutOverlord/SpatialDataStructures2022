## File Formats - Convert and Display City Data
#### Paige Champagne

This program reads in a geojson file of cities and a csv file of ufo sightings. It finds the distances between each of the cities and prints them to a json file, as well as reads in the ufo file and turns it into a geodataframe. For each of the cities, it finds the closest 100 ufo sightings and finds the average number of those 100 to find the average distance of the 100 closest ufo sightings to each city, and outputs that to a json file as well.

##### Files

|   #   | Folder Link | Assignment Description |
| :---: | ----------- | ---------------------- |
|   cities.geojson    |   [cities.geojson](P02/cities.geojson)          | geojson data file for cities   |
|   Cities.json    |   [Cities.json](P02/Cities.json)          | json final data file for cities with avg 100 closest ufo distance   |
|   program2.py    |   [program2.py](P02/program2.py)          | main file   |
|   tempCities.json    |   [tempCities.json](P02/tempCities.json)          | temp file for right after we originally read in cities from geojson. ignore.   |
|   tempDistances.json    |   [tempDistances.json](P02/tempDistances.json)          | json file with all the distances from each city to the other cities   |
|   ufo_data.csv    |   [ufo_data.csv](P02/ufo_data.csv)          |  csv file for ufo data  |