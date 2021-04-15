#!/usr/bin/python
#coding:utf-8

import requests
import shutil
import subprocess
import os
import sys
import argparse
import logging
from PIL import Image

nfoTemplate = """<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<movie>
  <title>%(movie_title)s</title>
  <originaltitle>%(movie_title)s</originaltitle>
  <sorttitle>%(movie_title)s</sorttitle>
  <set></set>
  <year></year>
  <top250></top250>
  <trailer></trailer>
  <votes></votes>
  <rating>%(movie_rate)s</rating>
  <outline></outline>
  <plot>%(movie_desc)s</plot>
  <tagline></tagline>
  <runtime></runtime>
  <releasedate>%(movie_date)s</releasedate>
  <studio>%(studio)s</studio>
  <thumb>%(poster)s</thumb>
  <fanart>
    <thumb>%(fanart)s</thumb>
  </fanart>
  <mpaa></mpaa>
  <id>%(mid)s</id>
  <genre></genre>
  %(actors)s
  <director></director>
</movie>"""

actorTemplate = """  <actor>
    <name>%(movie_star)s</name>
    <role></role>
    <thumb>%(movie_star_photo)s</thumb>
  </actor>
"""

studio = ""
actors = ""
movie_title = ""
movie_rate = ""
movie_desc = ""
movie_date = ""
poster_url = ""
fanart_url = ""

parser = argparse.ArgumentParser(description='Create NFO and poster/fanart.')
parser.add_argument('-i', '--inputfile', required=True, nargs=1, help=("Input Filename"))
parser.add_argument('-a', '--actors', action='append', required=True, help=("Actors"))
parser.add_argument('-m', '--movietitle', required=False, nargs=1, help=("Movie Title"))
parser.add_argument('-d', '--desc', required=False, nargs=1, help=("Description"))
parser.add_argument('-s', '--studio', required=False, nargs=1, help=("Studio"))
parser.add_argument('-p', '--poster', required=False, nargs=1, help=("Poster URL"))
parser.add_argument('-f', '--fanart', required=False, nargs=1, help=("Fanart URL"))
parser.add_argument('-r', '--releasedate', required=False, nargs=1, help=("Release Date"))

args = parser.parse_args()
logging.getLogger().setLevel(logging.INFO)
with open(args.inputfile[0], 'a'):
    pass
filename = os.path.split(args.inputfile[0])
os.chdir(filename[0])
fid, ext = os.path.splitext(filename[1])
logging.debug("pure file name %s" % fid)
logging.info("Proceed %s" % fid)

if not args.movietitle:
  movie_title = fid
else:
  movie_title = args.movietitle[0]

if not args.desc:
  movie_desc = movie_title
else:
  movie_desc = args.desc[0]

if not args.studio:
  studio = ""
else:
  studio = args.studio[0]

if not args.releasedate:
  movie_date = ""
else:
  movie_date = args.releasedate[0]

if not args.poster:
  poster_url = ""
else:
  poster_url = args.poster[0]
  poster = requests.get(poster_url, allow_redirects=True)
  with open(os.path.join('', fid +"-poster.jpg"), "wb") as posterfile:
    posterfile.write(poster.content)
  im = Image.open(fid+'-poster.jpg')
  if im.format == "WEBP":
     im.convert('RGB')
     im.save(fid+'-poster.jpg','jpeg')

if not args.fanart:
  fanart_url = ""
else:
  fanart_url = args.fanart[0]
  fanart = requests.get(fanart_url, allow_redirects=True)
  with open(os.path.join('', fid +"-fanart.jpg"), "wb") as fanrtfile:
    fanrtfile.write(fanart.content)
  im = Image.open(fid+'-fanart.jpg')
  if im.format == "WEBP":
     im.convert('RGB')
     im.save(fid+'-fanart.jpg','jpeg')

for actor in args.actors:
  logging.info("Add actor - %s" % actor)
  actors = actors + actorTemplate%{'movie_star': actor, 'movie_star_photo': ""}

nfoInfo = nfoTemplate%{'movie_title': movie_title,'movie_desc': movie_desc, 'movie_rate': "",
    'movie_date': movie_date, 'mid': fid, 'actors': actors, 'studio': studio, 'poster': poster_url, 'fanart': fanart_url}
with open(os.path.join('', fid +".nfo"), "w") as nfofile:
    nfofile.write(nfoInfo)
logging.info("%s NFO/Poster/Fanart Saved." % fid)
