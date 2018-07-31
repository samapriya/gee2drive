#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import csv
import shutil
from shutil import copyfile
from git import Repo
os.chdir(os.path.dirname(os.path.realpath(__file__)))
src = os.path.dirname(os.path.realpath(__file__))

# get os type

name = os.name

# set base folder names and paths

folder_name = 'eed'
pth = os.path.join(src, folder_name)

if name == 'nt':
    os.system('cls')
elif name == 'posix':
    os.system('clear')

if os.path.exists(pth):
    if name == 'nt':
        os.system('rmdir ' + '"' + pth + '" /s /q')
    elif name == 'posix':
        try:
            shutil.rmtree(pth)
        except:
            print 'Try using sudo privileges'

Repo.clone_from('https://github.com/samapriya/Earth-Engine-Datasets-List.git'
                , os.path.join(src, folder_name))

for items in os.listdir(os.path.join(src, folder_name)):
    if items.endswith('.csv'):
        copyfile(os.path.join(pth, items), os.path.join(src, items))
        with open(os.path.join(src, items)) as fp:
            reader = csv.reader(fp, delimiter=',')
            data = list(reader)
            row_count = len(data)
            print 'EE dataset updated and has ' + str(row_count) \
                + ' assets'
