import ee
import csv
import os
import json
import time
import sys
from kml2ee import kml2coord

os.chdir(os.path.dirname(os.path.realpath(__file__)))


try:
    ee.Initialize()
except Exception as e:
    sys.exit("Authenticate Earth Engine first and rerun program")


src = os.path.dirname(os.path.realpath(__file__))

l = []

for items in os.listdir(src):
    if items.endswith(".csv"):
        input_file = csv.DictReader(open(os.path.join(src, items)))
        for rows in input_file:
            l.append(rows["id"])


def intersect(start, end, geojson, operator, output):
    with open(output, "wb") as csvfile:
        writer = csv.DictWriter(
            csvfile, fieldnames=["type", "id", "#items"], delimiter=","
        )
        writer.writeheader()
    i = 1
    for items in l:
        print("Processing " + str(i) + " of " + str(len(l)))
        i = i + 1
        try:
            typ = ee.data.getInfo(items)["type"]
        except Exception as e:
            pass
        try:
            if geojson.endswith(".geojson"):
                with open(geojson) as aoi:
                    aoi_resp = json.load(aoi)
                    aoi_geom = ee.Geometry.Polygon(
                        aoi_resp["features"][0]["geometry"]["coordinates"]
                    )
                    boundbox = aoi_geom.bounds()
            elif geojson.endswith(".json"):
                with open(geojson) as aoi:
                    aoi_resp = json.load(aoi)
                    aoi_geom = ee.Geometry.Polygon(
                        aoi_resp["config"][0]["config"]["coordinates"]
                    )
                    boundbox = aoi_geom.bounds()
            elif geojson.endswith(".kml"):
                getcoord = kml2coord(geojson)
                aoi_geom = ee.Geometry.Polygon(getcoord)
                boundbox = aoi_geom.bounds()
        except Exception as e:
            print("Could not parse geometry")
            print(e)
        if str(typ) == "Image" and operator == "bb":
            try:
                userCollection = (
                    ee.ImageCollection([items])
                    .filterBounds(boundbox)
                    .filterDate(start, end)
                )
                length = userCollection.size().getInfo()
                if int(length) == 0:
                    pass
                    # print 'Geometry does not intersect collection '+str(items)
                else:
                    # print 'Total images in filtered collection: '+str(items) +' of size '+ str(length)
                    with open(output, "a") as csvfile:
                        writer = csv.writer(csvfile, delimiter=",", lineterminator="\n")
                        writer.writerow([str(typ), str(items), str(length)])
                    csvfile.close()
            except Exception as e:
                print("Check on Image failed becaused " + str(e))
        elif str(typ) == "Image" and operator == None:

            try:
                userCollection = (
                    ee.ImageCollection([items])
                    .filterBounds(aoi_geom)
                    .filterDate(start, end)
                )
                length = userCollection.size().getInfo()
                if int(length) == 0:
                    pass
                    # print 'Geometry does not intersect collection '+str(items)
                else:
                    # print 'Total images in filtered collection: '+str(items) +' of size '+ str(length)
                    with open(output, "a") as csvfile:
                        writer = csv.writer(csvfile, delimiter=",", lineterminator="\n")
                        writer.writerow([str(typ), str(items), str(length)])
                    csvfile.close()
            except Exception as e:
                print("Check on Image failed becaused " + str(e))
        elif typ == "ImageCollection" and operator == "bb":
            try:
                userCollection = (
                    ee.ImageCollection(items)
                    .filterBounds(boundbox)
                    .filterDate(start, end)
                )
                length = userCollection.size().getInfo()
                if int(length) == 0:
                    pass
                    # print 'Geometry does not intersect collection '+str(items)
                else:
                    # print 'Total images in filtered collection: '+str(items) +' of size '+ str(length)
                    with open(output, "a") as csvfile:
                        writer = csv.writer(csvfile, delimiter=",", lineterminator="\n")
                        writer.writerow([str(typ), str(items), str(length)])
                    csvfile.close()
            except Exception as e:
                print("Check on Collection failed becaused " + str(e))
        elif typ == "ImageCollection" and operator == None:
            try:
                userCollection = (
                    ee.ImageCollection(items)
                    .filterBounds(aoi_geom)
                    .filterDate(start, end)
                )
                length = userCollection.size().getInfo()
                if int(length) == 0:
                    pass
                    # print 'Geometry does not intersect collection '+str(items)
                else:
                    # print 'Total images in filtered collection: '+str(items) +' of size '+ str(length)
                    with open(output, "a") as csvfile:
                        writer = csv.writer(csvfile, delimiter=",", lineterminator="\n")
                        writer.writerow([str(typ), str(items), str(length)])
                    csvfile.close()
            except Exception as e:
                print("Check on Collection failed becaused " + str(e))
    print("")
    print("Report with Intersects Exported to " + str(output))


# exp(start='2000-01-01',end='2018-12-31',geojson=r'C:\planet_demo\terra\terra.geojson',operator=None,output=r'C:\planet_demo\terr.csv')
