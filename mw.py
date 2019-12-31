# -*- coding: UTF-8 -*-

import os
import argparse
import logging
import re
import shutil

logging.basicConfig(level=logging.INFO)

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

name_pattern = r'(\d{3})\s([^a-zA-Z]*)\s([a-zA-Z\s&]*)(【.*】)?'

def generate_nfo(folder_name, target_path):
    logging.info('Target Path: %s' %target_path)
    studio = "mywife.cc"
    actors = ""
    movie_title = ""
    movie_rate = ""
    movie_desc = ""
    movie_date = ""
    poster_url = ""
    fanart_url = ""

    name_match = re.search(name_pattern, folder_name)
    if name_match:
        _f_id = name_match.group(1)
        _f_actname = name_match.group(2)
        _f_act_e_name = name_match.group(3)
        _f_act = name_match.group(4)
        
        fid = 'Mywife-No00%s' % _f_id
        movie_title = 'Mywife No.%s %s' % (_f_id, _f_actname)
        movie_desc = movie_title
        actors = actors + actorTemplate%{'movie_star': _f_actname, 'movie_star_photo': ""}
        if _f_act is not None:
            actors = actors + actorTemplate%{'movie_star': _f_act.replace('】','').replace('【',''), 'movie_star_photo': ""}
        if _f_act_e_name is not None:
            actors = actors + actorTemplate%{'movie_star': _f_act_e_name, 'movie_star_photo': ""}    
        
        nfoInfo = nfoTemplate%{'movie_title': movie_title,'movie_desc': movie_desc, 'movie_rate': "",
            'movie_date': movie_date, 'mid': fid, 'actors': actors, 'studio': studio, 'poster': poster_url, 'fanart': fanart_url}
        
        logging.info(nfoInfo)
        with open(os.path.join(target_path, fid +".nfo"), "w") as nfofile:
            nfofile.write(nfoInfo)

        return fid
    return None
        
def generate_pics(fid, src_path, target_path):
    for (dirpath, dirnames, filenames) in os.walk(src_path):
        found = False
        for filename in filenames:
            if filename == 'top.jpg' and not found:
                destination = os.path.join(target_path, fid+'-fanart.jpg')
                dest = shutil.copyfile(os.path.join(src_path, filename), destination)
                found = True 
            elif filename == '001.jpg':
                destination = os.path.join(target_path, fid+'-poster.jpg')
                dest = shutil.copyfile(os.path.join(src_path, filename), destination) 
        if not found:
                destination = os.path.join(target_path, fid+'-fanart.jpg')
                dest = shutil.copyfile(os.path.join(src_path, '002.jpg'), destination)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', 
                       metavar='path',
                       type=str,
                       help='the path to proceed')

    parser.add_argument('-t', '--target_path', 
                       metavar='path',
                       type=str,
                       help='the target path')                   

    args = parser.parse_args()
    if not os.path.exists(args.target_path):
        os.mkdir(args.target_path)
        logging.info('target path %s created.' % args.target_path)
    logging.info('Target location: %s' % args.path) 
    for (dirpath, dirnames, filenames) in os.walk(args.path):
        for d in dirnames:
            logging.info('full path %s' % os.path.join(args.path, d))
            fid = generate_nfo(d, args.target_path)
            if (fid is not None):
                generate_pics(fid, os.path.join(args.path, d), args.target_path)

if __name__ == "__main__":
    main()