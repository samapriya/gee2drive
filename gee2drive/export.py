import ee
import os
import json
import time
import sys
try:
    ee.Initialize()
except Exception as e:
    print("Authenticate Earth Engine first and rerun program")
    time.sleep(2)
    os.system("earthengine authenticate")

def exp(collection,folderpath,start,end,geojson,bandnames):
    typ=ee.data.getInfo(collection)['type']
    if typ=="Image":
        with open (geojson) as aoi:
            aoi_resp=json.load(aoi)
            aoi_geom=ee.Geometry.Polygon(aoi_resp['features'][0]['geometry']['coordinates'])
        userCollection=ee.ImageCollection(collection).select(bandnames)
        clipname=os.path.basename(geojson).split('.')[0]
        fileName = str(collection).split('/')[-1]+'_'+str(clipname)
        firstband=ee.Image(collection).bandNames().getInfo()[0]
        scale=int(ee.Image(collection).select(firstband).projection().nominalScale().getInfo())
        task = ee.batch.Export.image.toDrive(
            image = ee.Image(collection).clip(aoi_geom),
            description = fileName,
            folder = folderpath,
            maxPixels = 1e13,
            region = aoi_geom.getInfo()['coordinates'][0],
            scale = scale)
        task.start()
        print('Finished creating export task')
        print('')
    elif typ=="ImageCollection":
        with open (geojson) as aoi:
            aoi_resp=json.load(aoi)
            aoi_geom=ee.Geometry.Polygon(aoi_resp['features'][0]['geometry']['coordinates'])
        userCollection=ee.ImageCollection(collection).filterBounds(aoi_geom).filterDate(start,end).select(bandnames)
        imageList = ee.List(userCollection.toList(userCollection.size().add(1)))
        length = userCollection.size().getInfo()
        if int(length)==0:
            print('No images found exiting export function')
            sys.exit()
        else:
            print("Total Image in filtered collection: "+str(length))
            def exportImage(img):
                fileName = ee.String(img.get('system:index')).getInfo()
                firstband=img.bandNames().getInfo()[0]
                scale=int(img.select(firstband).projection().nominalScale().getInfo())
                #get geometry of image
                task = ee.batch.Export.image.toDrive(
                    image = img.clip(aoi_geom),
                    description = fileName,
                    folder = folderpath,
                    maxPixels = 1e13,
                    region = aoi_geom.getInfo()['coordinates'][0],
                    scale = scale)
                task.start()

            index=0
            while index < int(length):
                print("Export #: " + str(index+1)+" of "+str(length))
                img2export = ee.Image(imageList.get(index))
                exportImage(img2export)
                index = index + 1
                #time.sleep(10)
            print('Finished creating export task')
            print('')
# exp(collection='USGS/SRTMGL1_003',#'ee.data.getInfo(args.asset_id)',
#        folderpath='ls-drive-exports',
#        start=None,end=None,
#        bandnames=['elevation'],
#        geojson=r'C:\Users\samapriya\Box Sync\IUB\Pycodes\Applications and Tools\Planet Tools\Standalone Tools\skysat-aoi\boulder.geojson')


#To get Bounding Box:img.geometry().bounds().getInfo()['coordinates'][0]
