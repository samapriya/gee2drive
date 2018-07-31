#!/usr/bin/python
# -*- coding: utf-8 -*-
import ee
import os
import time
import re
try:
    ee.Initialize()
except Exception, e:
    print 'Authenticate Earth Engine first and rerun program'
    time.sleep(2)
    os.system('earthengine authenticate')


##great alphanumeric sorting https://stackoverflow.com/questions/2669059/how-to-sort-alpha-numeric-set-in-python

def sorted_nicely(l):
    """ Sort the given iterable in the way that humans expect."""

    convert = lambda text: (int(text) if text.isdigit() else text)
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)'
                                , key)]
    return sorted(l, key=alphanum_key)


def imgexp(collection):
    typ = ee.data.getInfo(collection)['type']
    print typ + ' ' + str(collection)
    if typ == 'Image':
        info = ee.Image(collection).bandTypes().getInfo()
        b16uint = []
        b32uint = []
        b16sint = []
        b8uint = []
        fl = []
        for (key, value) in \
            ee.Image(collection).bandTypes().getInfo().items():
            if value['precision'] == 'float':
                fl.append(str(key))
            elif value['precision'] == 'int':
                if value['min'] == 0 and value['max'] == 255:
                    b8uint.append(str(key))
                if value['min'] == -32768 and value['max'] == 32767:
                    b16sint.append(str(key))
                if value['min'] == 0 and value['max'] == 65535:
                    b16uint.append(str(key))
                if value['min'] == 0 and value['max'] == 4294967295:
                    b32uint.append(str(key))
        if len(b8uint) > 0:
            print '8 bit unsigned integer bands ' + str(b8uint)
        if len(b16uint) > 0:
            print '16 bit unsigned integer bands ' \
                + str(sorted_nicely(b16uint))
        if len(b16sint) > 0:
            print '16 bit signed integer bands ' \
                + str(sorted_nicely(b16sint))
        if len(b32uint) > 0:
            print '32 bit unsigned integer bands ' \
                + str(sorted_nicely(b32uint))
        if len(fl) > 0:
            print 'Bands of type Float ' + str(fl)
    elif typ == 'ImageCollection':
        info = \
            ee.Image(ee.ImageCollection(collection).first()).getInfo()
        b16uint = []
        b32uint = []
        b16sint = []
        b8uint = []
        fl = []
        for (key, value) in \
            ee.Image(ee.ImageCollection(collection).first()).bandTypes().getInfo().items():
            if value['precision'] == 'float':
                fl.append(str(key))
            elif value['precision'] == 'int':

                if value['min'] == 0 and value['max'] == 255:
                    b8uint.append(str(key))
                if value['min'] == -32768 and value['max'] == 32767:
                    b16sint.append(str(key))
                if value['min'] == 0 and value['max'] == 65535:
                    b16uint.append(str(key))
                if value['min'] == 0 and value['max'] == 4294967295:
                    b32uint.append(str(key))
        if len(b8uint) > 0:
            print '8 bit unsigned integer bands ' + str(b8uint)
        if len(b16uint) > 0:
            print '16 bit unsigned integer bands ' \
                + str(sorted_nicely(b16uint))
        if len(b16sint) > 0:
            print '16 bit signed integer bands ' \
                + str(sorted_nicely(b16sint))
        if len(b32uint) > 0:
            print '32 bit unsigned integer bands ' \
                + str(sorted_nicely(b32uint))
        if len(fl) > 0:
            print 'Bands of type Float ' + str(fl)


# imgexp(collection='USGS/SRTMGL1_003')
