import geopandas
import csv
from shapely.geometry import box, Polygon, LineString, Point
file = open('ufo_data.csv')
type(file)
csvreader = csv.reader(file)
header = next(csvreader)
print(header)
ufos = {}
for h in header:
  if h not in ufos.keys():
    ufos[h] = []
for row in csvreader:
    ufos[h].append(row)
# print(rows)
file.close()

cities = geopandas.read_file('cities.geojson')
# ufos= geopandas.read_file('ufo_data.csv')
# print(cities)
# print(cities["geometry"])
# print(ufos)
# ufos.info()
# c = geopandas.GeoSeries(cities["geometry"])
keys = header
parallelUFOData = {}
for key in keys:
    parallelUFOData[key] = []
print(parallelUFOData)

# Every loop a new city is loaded into the "city" variable
for i in ufos:
    # print("ufo ", i)
    # Loop over the Keys that exist in our new parallel structure
    for key in parallelUFOData:
        
        print("key ", key)
        if key in i:
            parallelUFOData[key].append(i[key])
        else:
            parallelUFOData[key].append(None)

# print first five data elements in the newly formatted object
for key in parallelUFOData:
    print(parallelUFOData[key][:5])

# u = geopandas.GeoSeries(ufos)
# print(c.geometry.bounds)


# for i in cities:
#   for j in cities:
#     points_df = geopandas.GeoDataFrame({'geometry': [cities.iloc[[i]]["geometry"], cities.jloc[[j]]["geometry"]]}, crs='EPSG:4326')
#     points_df = points_df.to_crs('EPSG:5234')
#     points_df2 = points_df.shift()
#     points_df.distance(points_df2)
    # print(cities.iloc[[i]]["name"] cities.jloc[[j]]["geometry"])

# for i in ufos:
# u.sindex.nearest(c)
# print()
#   results = c.sindex.query(box(ufos["lon"]*20, ufos["lat"]*20, ufos["lon"]*-20, ufos["lat"]*-20))
  
#   for j in results:
#     # print(cities.jloc[[j]]["name"],ufos.jloc[[j]]["geometry"])
#     print(cities.jloc[[j]]["name"],cities.jloc[[j]]["geometry"])

