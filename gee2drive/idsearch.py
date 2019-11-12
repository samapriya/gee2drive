#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import csv

os.chdir(os.path.dirname(os.path.realpath(__file__)))
src = os.path.dirname(os.path.realpath(__file__))


def idsearch(mname):
    for items in os.listdir(src):
        if items.endswith('.csv'):
            input_file = csv.DictReader(open(os.path.join(src, items)))
            for rows in input_file:
                if mname.upper().lower() in str(rows['title'
                        ]).upper().lower():
                    try:
                        print str(rows['title']) + ' >> ' \
                            + str(rows['id'])
                    except Exception, e:
                        print e


# idsearch(mname='Belem')
