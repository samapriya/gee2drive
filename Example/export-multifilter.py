import ee
import os
import sys
import gee2drive
[head,tail]=os.path.split(gee2drive.__file__)
os.chdir(head)
sys.path.append(head)
from export import exp
ee.Initialize()
exp(collection=ee.ImageCollection('LANDSAT/LC08/C01/T1_SR').filterMetadata('CLOUD_COVER','less_than',20),folderpath="l8-out",start="2018-02-01",end="2018-06-01",geojson=r"C:\Users\samapriya\Box Sync\IUB\Pycodes\Applications and Tools\Planet Tools\Standalone Tools\skysat-aoi\boulder.geojson",bandnames="['B1','B2']",operator="bb",typ="ImageCollection")
