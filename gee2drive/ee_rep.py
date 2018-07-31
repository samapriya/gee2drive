#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import ee
import json
import csv
import subprocess
import os
pth = os.path.dirname(os.path.realpath(__file__))
ee.Initialize()

def ee_report(output):
    with open(output, 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['title', 'id'],
                                delimiter=',')
        writer.writeheader()
    a = subprocess.check_output('earthengine ls', shell=True)
    b = subprocess.check_output('earthengine ls -l -r ' + a, shell=True)
    try:
        for item in b.split('\n'):
            a = item.replace('[', '').replace(']', '').split()
            header = a[0]
            tail = a[1]
            if header == 'ImageCollection':
                collc = ee.ImageCollection(tail)
                print('Processing Image Collection ' + str(tail))
                with open(output, 'a') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',',
                            lineterminator='\n')
                    writer.writerow([str(tail).split('/')[-1], tail])
                csvfile.close()
            elif header == 'Image':
                collc = ee.Image(tail)
                print('Processing Image ' + str(tail))
                with open(output, 'a') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',',
                            lineterminator='\n')
                    writer.writerow([str(tail).split('/')[-1], tail])
                csvfile.close()
            else:
                pass
    except Exception:
        return 'worked'


ee_report(output=os.path.join(pth, 'myasset.csv'))

##if __name__ == '__main__':
##    ee_report(None)
