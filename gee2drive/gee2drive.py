#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
import glob
import subprocess
from idsearch import idsearch
from bandtypes import imgexp
from export import exp
from exp_report import intersect
os.chdir(os.path.dirname(os.path.realpath(__file__)))
path=os.path.dirname(os.path.realpath(__file__))
# Check if Earth Engine API is installed and authenticated

try:
    import ee
    ee.Initialize()
except Exception:
    print 'Initialize Earth Engine'
    subprocess.call('earthengine authenticate', shell=True)


def term():
    subprocess.call('python int_repl.py', shell=True)


def term_from_parser(args):
    term()


def refresh():
    filelist = glob.glob(os.path.join(path, "*.csv"))
    for f in filelist:
        os.remove(f)
    subprocess.call('python ee_rep.py', shell=True)
    subprocess.call('python gitcl.py', shell=True)


def refresh_from_parser(args):
    refresh()


def idsearch_from_parser(args):
    idsearch(mname=args.name)

def intersect_from_parser(args):
    intersect(start=args.start,
              end=args.end,
              geojson=args.aoi,
              operator=args.operator,
              output=args.report)

def imgexp_from_parser(args):
    imgexp(collection=args.id)


def exp_from_parser(args):
    exp(
        collection=args.id,
        folderpath=args.folder,
        typ=args.type,
        start=args.start,
        end=args.end,
        bandnames=args.bandlist,
        geojson=args.aoi,
        operator=args.operator,
        )
spacing = '                               '

def main(args=None):
    parser = \
        argparse.ArgumentParser(description='Google Earth Engine to Drive Exporter'
                                )

    subparsers = parser.add_subparsers()
    parser_term = subparsers.add_parser('terminal',
            help='Starts the interactive terminal with autosuggest')
    parser_term.set_defaults(func=term_from_parser)

    parser_refresh = subparsers.add_parser('refresh',
            help='Refreshes your personal asset list and GEE Asset list'
            )
    parser_refresh.set_defaults(func=refresh_from_parser)

    parser_idsearch = subparsers.add_parser('idsearch',
            help='Does possible matches using asset name to give you asseth id/full path'
            )
    parser_idsearch.add_argument('--name',
                                 help='Name or part of name to search for'
                                 )
    parser_idsearch.set_defaults(func=idsearch_from_parser)


    parser_intersect = subparsers.add_parser('intersect',
            help='Exports a report of all assets(Personal & GEE) intersecting with provided geometry')
    parser_intersect.add_argument('--start',
                                help='Start date to filter image',
                                default=None)
    parser_intersect.add_argument('--end', help='End date to filter image'
                                , default=None)
    parser_intersect.add_argument('--aoi',
                            help='Full path to geojson/json/kml to be used for bounds'
                            )
    parser_intersect.add_argument('--report',
                                help='Full path where the report will be exported including type, path & number of intersects'
                                , default=None)
    optional_named = \
    parser_intersect.add_argument_group('Optional named arguments for geometry only'
        )
    optional_named.add_argument('--operator',
                                help='Use bb for Bounding box incase the geometry is complex or has too many vertices'
                                , default=None)
    parser_intersect.set_defaults(func=intersect_from_parser)

    parser_imgexp = subparsers.add_parser('bandtype',
            help='Prints bandtype and generates list to be used for export'
            )
    parser_imgexp.add_argument('--id',
                               help='full path for collection or image')
    parser_imgexp.set_defaults(func=imgexp_from_parser)

    parser_exp = subparsers.add_parser('export',
            help='Export Collections based on filter')
    parser_exp.add_argument('--id',
                            help='Full path for collection or image')
    parser_exp.add_argument('--folder', help='Drive folder path')
    parser_exp.add_argument('--type',
                            help='Type whether image or collection')
    parser_exp.add_argument('--aoi',
                            help='Full path to geojson/json/kml to be used for bounds'
                            )
    optional_named = \
        parser_exp.add_argument_group('Optional named arguments for image collection only'
            )
    optional_named.add_argument('--start',
                                help='Start date to filter image',
                                default=None)
    optional_named.add_argument('--end', help='End date to filter image'
                                , default=None)
    optional_named.add_argument('--bandlist',
                                help='Bandlist we generated from bandtype export must be same bandtype'
                                , default=None)
    optional_named.add_argument('--operator',
                                help='Use bb for Bounding box incase the geometry is complex or has too many vertices'
                                , default=None)
    parser_exp.set_defaults(func=exp_from_parser)
    args = parser.parse_args()

    # ee.Initialize()

    args.func(args)


if __name__ == '__main__':
    main()
