# -*- coding: utf-8 -*-

import argparse
import os
import csv
import sys
import subprocess
import shutil
from shutil import copyfile
from git import Repo
from idsearch import idsearch
from bandtypes import imgexp
from export import exp
from exp_report import intersect

os.chdir(os.path.dirname(os.path.realpath(__file__)))
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)


# Check if Earth Engine API is installed and authenticated
try:
    import ee

    ee.Initialize()
except Exception:
    sys.exit("Initialize Earth Engine using: " + "\n" + "earthengine authenticate")


def refresh():
    print("Building assets cache. Hang on ..")
    for f in os.listdir(path):
        if f.endswith(".csv"):
            try:
                os.unlink(os.path.join(path, f))
            except WindowsError:
                with open(os.path.join(path, f), mode="w") as outfile:
                    outfile.close()
    # get os type
    name = os.name

    # set base folder names and paths
    folder_name = "eed"
    pth = os.path.join(path, folder_name)

    if os.path.exists(pth):
        if name == "nt":
            os.system("rmdir " + '"' + pth + '" /s /q')
        elif name == "posix":
            try:
                shutil.rmtree(pth)
            except:
                print("Try using sudo privileges")

    Repo.clone_from(
        "https://github.com/samapriya/Earth-Engine-Datasets-List.git",
        os.path.join(path, folder_name),
    )

    for items in os.listdir(os.path.join(path, folder_name)):
        if items.endswith(".csv"):
            copyfile(os.path.join(pth, items), os.path.join(path, items))

    # Get private assets from Google Earth Engine
    output = os.path.join(path, "myasset.csv")
    with open(output, "w") as csvfile:
        writer = csv.DictWriter(
            csvfile, fieldnames=["title", "id", "provider", "tags"], delimiter=","
        )
        writer.writeheader()
    a = subprocess.check_output("earthengine --no-use_cloud_api ls", shell=True)
    b = subprocess.check_output(
        "earthengine --no-use_cloud_api ls -l -r " + a, shell=True
    )
    try:
        for item in b.split("\n"):
            a = item.replace("[", "").replace("]", "").split()
            header = a[0]
            tail = a[1]
            if header == "ImageCollection":
                collc = ee.ImageCollection(tail)
                # print("Processing Image Collection " + str(tail))
                with open(output, "a") as csvfile:
                    writer = csv.writer(csvfile, delimiter=",", lineterminator="\n")
                    writer.writerow([str(tail).split("/")[-1], tail])
                csvfile.close()
            elif header == "Image":
                collc = ee.Image(tail)
                # print("Processing Image " + str(tail))
                with open(output, "a") as csvfile:
                    writer = csv.writer(csvfile, delimiter=",", lineterminator="\n")
                    writer.writerow([str(tail).split("/")[-1], tail])
                csvfile.close()
            elif header == "Table":
                collc = ee.FeatureCollection(tail)
                # print("Processing Image " + str(tail))
                with open(output, "a") as csvfile:
                    writer = csv.writer(csvfile, delimiter=",", lineterminator="\n")
                    writer.writerow([str(tail).split("/")[-1], tail])
                csvfile.close()
            else:
                pass
    except Exception as e:
        pass

    for f in os.listdir(path):
        if f.endswith(".csv"):
            if f.startswith("myasset"):
                lt = 0
                with open(os.path.join(path, f), "r") as f:
                    reader = csv.reader(f, delimiter=",")
                    data = list(reader)
                    row_count = sum(1 for row in data)
                    lt = lt + row_count
                    print("Total private assets: " + str(lt - 1))
            else:
                lt = 0
                with open(os.path.join(path, f), "r") as f:
                    reader = csv.reader(f, delimiter=",")
                    data = list(reader)
                    row_count = sum(1 for row in data)
                    lt = lt + row_count
                    print("Total ee-catalog assets: " + str(lt - 1))
    print("Cache Built")


def refresh_from_parser(args):
    refresh()


def idsearch_from_parser(args):
    idsearch(mname=args.name)


def intersect_from_parser(args):
    intersect(
        start=args.start,
        end=args.end,
        geojson=args.aoi,
        operator=args.operator,
        output=args.report,
    )


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
        ff=args.ftype,
    )


spacing = "                               "


def main(args=None):
    parser = argparse.ArgumentParser(
        description="Google Earth Engine to Drive Exporter"
    )

    subparsers = parser.add_subparsers()

    parser_refresh = subparsers.add_parser(
        "refresh", help="Refreshes your personal asset list and GEE Asset list"
    )
    parser_refresh.set_defaults(func=refresh_from_parser)

    parser_idsearch = subparsers.add_parser(
        "idsearch",
        help="Does possible matches using asset name to give you asseth id/full path",
    )
    parser_idsearch.add_argument(
        "--name",
        help="Name or part of name to search for, or tag or provider or asset id",
    )
    parser_idsearch.set_defaults(func=idsearch_from_parser)

    parser_intersect = subparsers.add_parser(
        "intersect",
        help="Exports a report of all assets(Personal & GEE) intersecting with provided geometry",
    )
    parser_intersect.add_argument(
        "--start", help="Start date to filter image", default=None
    )
    parser_intersect.add_argument(
        "--end", help="End date to filter image", default=None
    )
    parser_intersect.add_argument(
        "--aoi", help="Full path to geojson/json/kml to be used for bounds"
    )
    parser_intersect.add_argument(
        "--report",
        help="Full path where the report will be exported including type, path & number of intersects",
        default=None,
    )
    optional_named = parser_intersect.add_argument_group(
        "Optional named arguments for geometry only"
    )
    optional_named.add_argument(
        "--operator",
        help="Use bb for Bounding box incase the geometry is complex or has too many vertices",
        default=None,
    )
    parser_intersect.set_defaults(func=intersect_from_parser)

    parser_imgexp = subparsers.add_parser(
        "bandtype", help="Prints bandtype and generates list to be used for export"
    )
    parser_imgexp.add_argument("--id", help="full path for collection or image")
    parser_imgexp.set_defaults(func=imgexp_from_parser)

    parser_exp = subparsers.add_parser(
        "export", help="Export Collections based on filter"
    )
    parser_exp.add_argument("--id", help="Full path for collection or image or table")
    parser_exp.add_argument("--folder", help="Drive folder path")
    parser_exp.add_argument("--type", help="Type whether image or collection or table")
    parser_exp.add_argument(
        "--aoi", help="Full path to geojson/json/kml to be used for bounds"
    )
    optional_named = parser_exp.add_argument_group(
        "Optional named arguments for image collection only"
    )
    optional_named.add_argument(
        "--start", help="Start date to filter image", default=None
    )
    optional_named.add_argument("--end", help="End date to filter image", default=None)
    optional_named.add_argument(
        "--bandlist",
        help="Bandlist we generated from bandtype export must be same bandtype",
        default=None,
    )
    optional_named.add_argument(
        "--operator",
        help="Use bb for Bounding box incase the geometry is complex or has too many vertices",
        default=None,
    )
    optional_named.add_argument(
        "--ftype",
        help="Used only for exporting table choose SHP, KML, KMZ, GeoJSON, TFRECORD",
        default=None,
    )
    parser_exp.set_defaults(func=exp_from_parser)
    args = parser.parse_args()

    # ee.Initialize()

    args.func(args)


if __name__ == "__main__":
    main()
