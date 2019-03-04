#!/usr/bin/python
#coding:utf-8

import scrapy
import os
import subprocess
import urlparse
import logging
import requests
import shutil
import re
from scrapy_splash import SplashRequest

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

title_XPath = "//h3[contains(@class,'h1')]/text()"
poster_url_XPath = "//div[contains(@class,'about-author')]/a/img/@src"
fanart_url_XPath = "//div[contains(@class,'content-cover')]/img/@src"
desc_XPath = "//div[contains(@class,'blog-single')]/p/text()"
actros_XPath = "//div[contains(@class,'about-author')]//h5/text()"
date_XPath = "//div[contains(@class,'single-meta')]//span[contains(@class,'date')]/text()" #the date is the 5th

logging.getLogger().setLevel(logging.INFO)

class ScuteSpider(scrapy.Spider):
    name = "scute"    
    fid = ""
    s_id = ""
    studio = ""
    actors = ""
    movie_title = ""
    movie_rate = ""
    movie_desc = ""
    movie_date = ""
    poster_url = ""
    fanart_url = ""
    movie_star_photo = ""

    def __init__(self, fid, *args, **kwargs):
        self.fid = fid
        super(ScuteSpider, self).__init__(*args, **kwargs)
        self.baseUrl = 'http://www.s-cute.com/contents/'+ self.fid + '/'
        print "proceed %s" % self.baseUrl

    def start_requests(self):
        urls = [
            self.baseUrl
        ]

        script = """
        function main(splash)
            assert(splash:go(splash.args.url))
            return {html=splash:html()}
        end
        """

        for url in urls:
            yield SplashRequest(url=url, callback=self.parse, endpoint='execute', args={'wait': 0.5, 'lua_source':script})

    def parse(self, response):
        print response
        self.movie_title = self.fid + ' ' + response.xpath(title_XPath).extract_first().strip()
        print "Title --> %s" % self.movie_title.encode('utf-8')
        self.poster_url = response.xpath(poster_url_XPath).extract_first()
        self.movie_star_photo = self.poster_url
        self.poster_url = self.poster_url.replace('_150.jpg','_400.jpg')
        print "Poster url ---> %s" % self.poster_url
        rposter = requests.get(self.poster_url, stream=True)
        poster_path = self.fid + "-poster.jpg"
        if rposter.status_code == 200:
            with open(os.path.join('alldone/',poster_path), 'wb') as f0:
                rposter.raw.decode_content = True
                shutil.copyfileobj(rposter.raw, f0) 
        print "poster saved."
        self.fanart_url = response.xpath(fanart_url_XPath).extract_first()
        print "Fanart url --> %s" % self.fanart_url
        rfanart = requests.get(self.fanart_url, stream=True)
        fanart_path = self.fid + "-fanart.jpg"
        if rfanart.status_code == 200:
            with open(os.path.join('alldone/',fanart_path), 'wb') as f0:
                rfanart.raw.decode_content = True
                shutil.copyfileobj(rfanart.raw, f0) 
        self.movie_desc = response.xpath(desc_XPath).extract_first()
        print "Desc ---> %s" % self.movie_desc.encode('utf-8')

        actor = response.xpath(actros_XPath).extract_first().replace('"','').strip()      
        self.actors = actorTemplate%{'movie_star': actor, 'movie_star_photo': self.movie_star_photo}
        print "Actor --> %s" %self.actors.encode('utf-8')

        self.movie_date = response.xpath(date_XPath).extract_first().encode('utf-8').replace('公開日 ','')
        print "Date --> %s" % self.movie_date
       
        nfoInfo = nfoTemplate%{'movie_title': self.movie_title,'movie_desc': self.movie_desc, 'movie_rate': "",
            'movie_date': self.movie_date, 'mid': self.fid, 'actors': self.actors, 'studio': "", 'poster': self.poster_url, 'fanart': self.fanart_url}
        with open(os.path.join('alldone/', self.fid +".nfo"), "w") as nfofile:
            nfofile.write(nfoInfo.encode('utf-8'))
        print "%s NFO/Poster/Fanart Saved." % self.fid

    def closed(self, reason):
        pass