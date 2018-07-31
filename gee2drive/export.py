import ee
import os
import json
import time
import sys
import ast

try:
    ee.Initialize()
except Exception, e:
    print 'Authenticate Earth Engine first and rerun program'
    time.sleep(2)
    os.system('earthengine authenticate')


def exp(collection,folderpath,start,end,
    geojson,bandnames,operator,typ):
    #typ = ee.data.getInfo(collection)['type']
    bandnames = ast.literal_eval(bandnames)
    if typ == 'image' and operator == 'bb':
        with open(geojson) as aoi:
            aoi_resp = json.load(aoi)
            aoi_geom = ee.Geometry.Polygon(aoi_resp['features'
                    ][0]['geometry']['coordinates'])
            boundbox = aoi_geom.bounds()
        userCollection = \
            ee.ImageCollection(collection).select(bandnames)
        clipname = os.path.basename(geojson).split('.')[0]
        fileName = str(collection).split('/')[-1] + '_' + str(clipname) \
            + '_bb'
        firstband = ee.Image(collection).bandNames().getInfo()[0]
        scale = \
            int(ee.Image(collection).select(firstband).projection().nominalScale().getInfo())
        task = ee.batch.Export.image.toDrive(
            image=ee.Image(collection).clip(boundbox),
            description=fileName,
            folder=folderpath,
            maxPixels=1e13,
            region=boundbox.getInfo()['coordinates'][0],
            scale=scale,
            )
        task.start()
        print 'Finished creating export task'
        print ''
    elif typ == 'image' and operator == None:
        with open(geojson) as aoi:
            aoi_resp = json.load(aoi)
            aoi_geom = ee.Geometry.Polygon(aoi_resp['features'
                    ][0]['geometry']['coordinates'])
        userCollection = \
            ee.ImageCollection(collection).select(bandnames)
        clipname = os.path.basename(geojson).split('.')[0]
        fileName = str(collection).split('/')[-1] + '_' + str(clipname)
        firstband = ee.Image(collection).bandNames().getInfo()[0]
        scale = \
            int(ee.Image(collection).select(firstband).projection().nominalScale().getInfo())
        task = ee.batch.Export.image.toDrive(
            image=ee.Image(collection).clip(aoi_geom),
            description=fileName,
            folder=folderpath,
            maxPixels=1e13,
            region=aoi_geom.getInfo()['coordinates'][0],
            scale=scale,
            )
        task.start()
        print 'Finished creating export task'
        print ''
    elif typ == 'collection' and operator == 'bb':
        with open(geojson) as aoi:
            aoi_resp = json.load(aoi)
            aoi_geom = ee.Geometry.Polygon(aoi_resp['features'
                    ][0]['geometry']['coordinates'])
            boundbox = aoi_geom.bounds()
        userCollection = \
            ee.ImageCollection(collection).filterBounds(aoi_geom).filterDate(start,
                end).select(bandnames)
        clipname = os.path.basename(geojson).split('.')[0]
        imageList = \
            ee.List(userCollection.toList(userCollection.size().add(1)))
        length = userCollection.size().getInfo()
        if int(length) == 0:
            print 'No images found exiting export function'
            sys.exit()
        else:
            print 'Total images in filtered collection: ' + str(length)

            def exportImage(img):
                fileName = ee.String(img.get('system:index')).getInfo()
                firstband = img.bandNames().getInfo()[0]
                scale = \
                    int(img.select(firstband).projection().nominalScale().getInfo())

                # get geometry of image

                task = ee.batch.Export.image.toDrive(
                    image=img.clip(boundbox),
                    description=fileName + '_' + str(clipname) + '_bb',
                    folder=folderpath,
                    maxPixels=1e13,
                    region=boundbox.getInfo()['coordinates'][0],
                    scale=scale,
                    )
                task.start()

            index = 0
            while index < int(length):
                print 'Export #: ' + str(index + 1) + ' of ' \
                    + str(length)
                img2export = ee.Image(imageList.get(index))
                exportImage(img2export)
                index = index + 1

                # time.sleep(10)

            print 'Finished creating export task'
            print ''
    elif typ == 'collection' and operator == None:
        with open(geojson) as aoi:
            aoi_resp = json.load(aoi)
            aoi_geom = ee.Geometry.Polygon(aoi_resp['features'
                    ][0]['geometry']['coordinates'])
        userCollection = \
            ee.ImageCollection(collection).filterBounds(aoi_geom).filterDate(start,
                end).select(bandnames)
        clipname = os.path.basename(geojson).split('.')[0]
        imageList = \
            ee.List(userCollection.toList(userCollection.size().add(1)))
        length = userCollection.size().getInfo()
        if int(length) == 0:
            print 'No images found exiting export function'
            sys.exit()
        else:
            print 'Total images in filtered collection: ' + str(length)

            def exportImage(img):
                fileName = ee.String(img.get('system:index')).getInfo()
                firstband = img.bandNames().getInfo()[0]
                scale = \
                    int(img.select(firstband).projection().nominalScale().getInfo())

                # get geometry of image

                task = ee.batch.Export.image.toDrive(
                    image=img.clip(aoi_geom),
                    description=fileName + '_' + str(clipname),
                    folder=folderpath,
                    maxPixels=1e13,
                    region=aoi_geom.getInfo()['coordinates'][0],
                    scale=scale,
                    )
                task.start()

            index = 0
            while index < int(length):
                print 'Export #: ' + str(index + 1) + ' of ' \
                    + str(length)
                img2export = ee.Image(imageList.get(index))
                exportImage(img2export)
                index = index + 1

                # time.sleep(10)

            print 'Finished creating export task'
            print ''
