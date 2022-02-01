## File Formats - Convert and Display City Data
#### Paige Champagne

The basic idea behind this program is to use Python to read in one file and output another.
Uses a .json file to read in city data. It then:
- Only evaluates those cities in the continental United States (no Hawaii or Alaska).
- Identifie the largest city in each state.
- After the most populated cities are found (49 of them) orders the cities from west to east.
- Turns each city into a Point that is placed into a features list in a geoJson file.
- Each city has a randomly (or some other coloring scheme) colored marker that is numbered by its order from west to east.
- Creates a LineString connecting each city and place that in your features list as well.

##### Files

|   #   | Folder Link | Assignment Description |
| :---: | ----------- | ---------------------- |
|   program1.py    |   [program1.py](P01/program1.py)          | main file   |
|   cities.json    |   [cities.json](P01/cities.json)          | json data file   |
|   new.geojson    |   [new.geojson](P01/new.geojson)          | new geojson file   |