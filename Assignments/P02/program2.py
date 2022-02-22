import geopandas
from shapely.geometry import box, Polygon, LineString, Point

df = geopandas.read_file('cities.geojson')
print(df)