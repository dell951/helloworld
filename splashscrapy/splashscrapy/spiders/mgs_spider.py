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

title_XPath = "//h1[contains(@class,'tag')]/text()"
poster_url_XPath = "//div[contains(@class,'detail_photo') or contains(@class,'detail_data')]//img/@src"
fanart_url_XPath = "//dl//a[contains(@class,'sample_image')]/@href"
desc_XPath = "//p[contains(@class,'txt introduction')]/text()"
actros_XPath = "//table/tbody/tr/th/../td/a/text()" #will get the first one as the actor
date_XPath = "//table/tbody/tr/th/../td" #the date is the 5th

logging.getLogger().setLevel(logging.INFO)

class MgsSpider(scrapy.Spider):
    name = "mgs"    
    fid = ""
    studio = ""
    actors = ""
    movie_title = ""
    movie_rate = ""
    movie_desc = ""
    movie_date = ""
    poster_url = ""
    fanart_url = ""

    def __init__(self, fid, *args, **kwargs):
        self.fid = fid
        print "proceed %s..." % fid
        super(MgsSpider, self).__init__(*args, **kwargs)
        self.baseUrl = 'https://www.mgstage.com/product/product_detail/'+ self.fid.upper() + '/'
       
    def start_requests(self):
        urls = [
            self.baseUrl
        ]

        script = """
        function main(splash)
            assert(splash:go(splash.args.url))
            splash:evaljs("document.getElementById('AC').click()")
            splash:wait(10)
            return {html=splash:html()}
        end
        """

        for url in urls:
            yield SplashRequest(url=url, callback=self.parse, endpoint='execute', args={'wait': 0.5, 'lua_source':script})

    def parse(self, response):
        self.movie_title = self.fid + ' ' + response.xpath(title_XPath).extract_first().strip()
        print self.movie_title.encode('utf-8')
        self.poster_url = response.xpath(poster_url_XPath).extract_first()
        print self.poster_url
        rposter = requests.get(self.poster_url, stream=True)
        poster_path = self.fid + "-poster.jpg"
        if rposter.status_code == 200:
            with open(os.path.join('alldone/',poster_path), 'wb') as f0:
                rposter.raw.decode_content = True
                shutil.copyfileobj(rposter.raw, f0) 

        self.fanart_url = response.xpath(fanart_url_XPath).extract_first()
        rfanart = requests.get(self.fanart_url, stream=True)
        fanart_path = self.fid + "-fanart.jpg"
        if rfanart.status_code == 200:
            with open(os.path.join('alldone/',fanart_path), 'wb') as f0:
                rfanart.raw.decode_content = True
                shutil.copyfileobj(rfanart.raw, f0) 
        print self.fanart_url
        self.movie_desc = response.xpath(desc_XPath).extract_first()
        print self.movie_desc.encode('utf-8')
        try:
            actor = response.xpath(actros_XPath).extract_first().replace('"','').strip().split()[0]
        except:
            actor = response.xpath(actros_XPath).extract_first().replace('"','').strip()
        
        self.actors = actorTemplate%{'movie_star': actor, 'movie_star_photo': ""}
        print self.actors.encode('utf-8')
        #self.movie_date = response.xpath(date_XPath).extract()
        briefs = response.xpath(date_XPath).extract()
        details = ""
        for item in briefs:
            details = details + item
        datesection = re.findall("<td>20\d\d\/\d\d\/\d\d</td>", details)
        if datesection:
            self.movie_date = datesection[0].replace('<td>','').replace('</td>','').replace('/','-')
        nfoInfo = nfoTemplate%{'movie_title': self.movie_title,'movie_desc': self.movie_desc, 'movie_rate': "",
            'movie_date': self.movie_date, 'mid': self.fid, 'actors': self.actors, 'studio': "", 'poster': self.poster_url, 'fanart': self.fanart_url}
        with open(os.path.join('alldone/', self.fid +".nfo"), "w") as nfofile:
            nfofile.write(nfoInfo.encode('utf-8'))
        print "%s NFO/Poster/Fanart Saved." % self.fid

    def closed(self, reason):
        pass
