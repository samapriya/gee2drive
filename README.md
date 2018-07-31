# gee2drive: Download Earth Engine Public and Private assets to Google Drive

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1324456.svg)](https://doi.org/10.5281/zenodo.1324456)
[![PyPI version](https://badge.fury.io/py/gee2drive.svg)](https://badge.fury.io/py/gee2drive)

Google Earth Engine currently allows you to export images and assets as either GeoTiff files or TFrecords. The system splits the files if the estimated size is greater than 2GB which is the upper limit and needs the geometry to be parsed in the form of either a fusion table, a user drawn geometry or a table imported into the user's assets. While the javascript frontend is great owing to the queryable catalog whereby you can search and and export your personal and private assets, the limitation lies in batch exports. To resolve this the python API access allows you to call batch export functions but now it is limited to checking for itersects first and running without having a queryable catalog. With the same idea I created this tool which allows you to run a terminal environment where your personal and general catalog images are part of a autosuggest feature. This tool allows you to look for images based on names for example " you can search for Sentinel and it will show you full path of images which have the word sentinel in the title". It also creates a report for your image collections and images so apart from the public datasets this can also find your own datasets as well. You can then generate bandlist to make sure all bands you are exporting are of the same type and then export all images that intersect you aoi.

The assumption here is
* Every image in the give image have the same band structure, choose the bandlist that you know to common to all images
* If the geomery is too complex use the operator feature to use a bounding box instead.
* For now all it filters is geometry and date, and it is does not filter based on metadata (however in the examples folder I have shown how to import and use additional filter before exporting an image collection)

In the future I will try to integrate some other functionalities to this environment and you can indeed run the tool without the use of the autosuggest terminal as a simple CLI. Hence the terminal feature is optional.

## Table of contents
* [Installation](#installation)
* [Getting started](#getting-started)
* [Google Earth Engine to Drive Manager](#google-earth-engine-to-drive-manager)
	* [GEE to Google Drive CLI](#gee-to-google-drive-cli)
    * [gee2drive Terminal](#gee2drive-terminal)
    * [gee2drive refresh](#gee2drive-refresh)
    * [gee2drive idsearch](#gee2drive-idsearch)
    * [gee2drive bandtype](#gee2drive-bandtype)
    * [gee2drive export](#gee2drive-export)

## Installation
This assumes that you have native python & pip installed in your system, you can test this by going to the terminal (or windows command prompt) and trying. This assumes that you are also well aware of Google Earth Engine Python setup and have it installed and authetenticated on your system. If not you can [read about it here](https://developers.google.com/earth-engine/python_install_manual)

```python``` and then ```pip list```

If you get no errors and you have python 2.7.14 or higher you should be good to go. Please note that I have tested this only on python 2.7.15 but can be easily modified for python 3.

To install **Python CLI for Digital Ocean** you can install using two methods

```pip install gee2drive```

or you can also try

```
git clone https://github.com/samapriya/gee2drive.git
cd gee2drive
python setup.py install
```

Use might have to use sudo privileges

Installation is an optional step; the application can be also run directly by executing gee2drive.py script. The advantage of having it installed is being able to execute ppipe as any command line tool. I recommend installation within virtual environment. If you don't want to install, browse into the gee2drive folder and try ```python gee2drive.py``` to get to the same result.

![cli](/images/gee2drive.gif)

## Getting started

As usual, to print help:

```
usage: gee2drive [-h] {terminal,refresh,idsearch,bandtype,export} ...

Google Earth Engine to Drive Exporter

positional arguments:
  {terminal,refresh,idsearch,bandtype,export}
    terminal            Starts the interactive terminal with autosuggest
    refresh             Refreshes your personal asset list and GEE Asset list
    idsearch            Does possible matches using asset name to give you
                        asseth id/full path
    bandtype            Prints bandtype and generates list to be used for
                        export
    export              Export Collections based on filter

optional arguments:
  -h, --help            show this help message and exit

```

To obtain help for a specific functionality, simply call it with _help_ switch, e.g.: `gee2drive idsearch -h`. If you didn't install gee2drive, then you can run it just by going to *gee2drive* directory and running `python gee2drive.py [arguments go here]`

### GEE to Google Drive CLI
This tool is designed to augment to the existing facilty of image export using a CLI, whereby you can pass it arguments to filter based on an area of interest geojson file, a start and end date for collection

### gee2drive Terminal
This is an autosuggestive terminal which uses the gee2add package to perform all of the functions but has autosuggest for Earth Engine catalog and your own personal catalog. This way you can get access to image id without needing the catalog id in the javascript codeeditor.

```
usage: gee2drive terminal [-h]

optional arguments:
  -h, --help  show this help message and exit
```

![cli](/images/terminal.gif)

Once you type ```gee2drive terminal``` you get a shell inside your current terminal where you get autosuggest for image and have full functionality of the terminal.


### gee2drive refresh
For the past couple of months I have [maintained a catalog of the most current Google Earth Engine assets](https://github.com/samapriya/Earth-Engine-Datasets-List), within their raster data catalog. I update this list every week. This tool downloads the most current version of this list, and also looks into your personal assets to generate your very own asset report which then serve as a master dataset to feed into autosuggestions.

```
gee2drive refresh -h
usage: gee2drive refresh [-h]

optional arguments:
  -h, --help  show this help message and exit
```

### gee2drive idsearch
There is a possibility that you don't really remember the full path to your asset or the public asset. Fortunately when I parse and collect the image list and path for you they have names that are searchable so use a keyword. for example search using "MODIS" or "sentinel". Also it is not case sensitive, so you should be able to type "SENTINEl" or "Sentinel" or "sentinel" and it should still work

```
gee2drive idsearch -h
usage: gee2drive idsearch [-h] [--name NAME]

optional arguments:
  -h, --help   show this help message and exit
  --name NAME  Name or part of name to search for
```

### gee2drive bandtype
Export requires all the bandtypes to be of the same kind. To do this, I simply generate the band types for you and you can select the band list you want , remember to paste it as a list.

```
usage: gee2drive bandtype [-h] [--id ID]

optional arguments:
  -h, --help  show this help message and exit
  --id ID     full path for collection or image
```

### gee2drive export
Finally the export tool, that lets you export an image or a collection clipped to your AOI. This makes use of the bandlist you exported. Incase you are exporting an image and not a collection you don't need a start and end date. The tool uses the bounds() function to use a bounding box incase the geometry has a complex geometry or too many vertices simply use the operator ```bb```. If the geojson/json/kml keeps giving parsing error go to [geojson.io](geojson.io)

```
usage: gee2drive export [-h] [--id ID] [--type TYPE] [--folder FOLDER]
                        [--aoi AOI] [--start START] [--end END]
                        [--bandlist BANDLIST] [--operator OPERATOR]

optional arguments:
  -h, --help           show this help message and exit
  --id ID              Full path for collection or image
  --type TYPE          Type whether image or collection
  --folder FOLDER      Drive folder path
  --aoi AOI            Full path to geojson/json/kml to be used for bounds

Optional named arguments for image collection only:
  --start START        Start date to filter image
  --end END            End date to filter image
  --bandlist BANDLIST  Bandlist we generated from bandtype export must be same
                       bandtype
  --operator OPERATOR  Use bb for Bounding box incase the geometry is complex
                       or has too many vertices
```

A typical setup would be
```gee2drive export --id "COPERNICUS/S2" --folder "sentinel-export" --aoi "C:\Users\sam\boulder.geojson" --start "2018-02-01" --end "2018-03-01"
--bandlist ['B2','B3','B4'] --operator "bb" --type "collection"
```

Also as promised earlier , there is a way to add additional filters and then pass it through the export function here is how and I have included this in the Examples folder. This for example uses the Landsat collection but applies the Cloud cover filter before passing it for export

```python
import ee
import os
import sys
import gee2drive
[head,tail]=os.path.split(gee2drive.__file__)
os.chdir(head)
sys.path.append(head)
from export import exp
ee.Initialize()
exp(collection=ee.ImageCollection('LANDSAT/LC08/C01/T1_SR').filterMetadata('CLOUD_COVER','less_than',20),
    folderpath="l8-out",start="2018-02-01",end="2018-06-01",
    geojson=r"C:\Users\sam\boulder.geojson",bandnames="['B1','B2']",
    operator="bb",typ="ImageCollection")
```


#### Changelog

##### v0.0.4
* Can now parse gejson, json,kml
* Minor fixes and general improvements

##### v0.0.3
* Minor Fixes
