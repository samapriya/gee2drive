#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import csv
from prettytable import PrettyTable

os.chdir(os.path.dirname(os.path.realpath(__file__)))
src = os.path.dirname(os.path.realpath(__file__))

x = PrettyTable()


def idsearch(mname):
    for items in os.listdir(src):
        if items.endswith(".csv"):
            i = 1
            input_file = csv.DictReader(open(os.path.join(src, items)))
            for rows in input_file:
                if mname.lower() in str(rows["title"]).lower():
                    try:
                        x.field_names = ["index", "name", "id"]
                        x.add_row([i, rows["title"], rows["id"]])
                        i = i + 1
                    except Exception as e:
                        print(e)
                elif mname.lower() in str(rows["id"]).lower():
                    try:
                        x.field_names = ["index", "name", "id"]
                        x.add_row([i, rows["title"], rows["id"]])
                        i = i + 1
                    except Exception as e:
                        print(e)
                elif mname.lower() in str(rows["provider"]).lower():
                    try:
                        x.field_names = ["index", "name", "id"]
                        x.add_row([i, rows["title"], rows["id"]])
                        i = i + 1
                    except Exception as e:
                        print(e)
                elif mname.lower() in str(rows["tags"]).lower():
                    try:
                        x.field_names = ["index", "name", "id"]
                        x.add_row([i, rows["title"], rows["id"]])
                        i = i + 1
                    except Exception as e:
                        print(e)
    print(x)


# idsearch(mname='Belem')
