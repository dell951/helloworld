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
from scrapy.selector import HtmlXPathSelector

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

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'
movie_XPath = "//div[contains(@class,'Container')]//div[contains(@class,'Column')]//section"

title_XPath = "//h3[contains(@class,'h1')]/text()"
poster_url_XPath = ""
fanart_url_XPath = "//div[contains(@class,'content-cover')]/img/@src"
desc_XPath = "//div[contains(@class,'blog-single')]/p/text()"
actros_XPath = "//div[contains(@class,'about-author')]//h5/text()"
date_XPath = "//div[contains(@class,'single-meta')]//span[contains(@class,'date')]/text()" #the date is the 5th

logging.getLogger().setLevel(logging.INFO)

class BabesSpider(scrapy.Spider):
    name = "babes"    
    fid = ""
    movie_id = ""
    studio = "Babes"
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
        self.movie_id = fid.split('/')[3]
        super(BabesSpider, self).__init__(*args, **kwargs)
        self.baseUrl = 'https://www.' + self.studio + '.com'+ self.fid
        print "proceed %s" % self.baseUrl

    def start_requests(self):
        urls = [
            self.baseUrl
        ]

        script = """
        function main(splash)
            assert(splash:go(splash.args.url))
            assert(splash:wait(5.5))
            return {html=splash:html()}
        end
        """

        for url in urls:
            print url
            yield SplashRequest(url=url, callback=self.parse, endpoint='execute', args={'wait': 5.5, 'lua_source':script})

    def parse(self, response):
        #print response.text
        hxs = HtmlXPathSelector(response)
        movie_item = hxs.select(movie_XPath)[0]
        self.movie_title = movie_item.select('.//h2/text()').extract_first().strip()
        print "Title --> %s" % self.movie_title.encode('utf-8')
        self.poster_url = movie_item.select('.//img/@src').extract_first()
        self.movie_star_photo = self.poster_url
        print "Poster url ---> %s" % self.poster_url
        #headers = {'User-Agent': user_agent}
        #rposter = requests.get(self.poster_url, headers=headers)
        poster_path = 'alldone/' + self.movie_id + "-poster.jpg"
        #if rposter.status_code == 200:
        #    with open(os.path.join('alldone/',poster_path), 'wb') as f0:
        #        rposter.raw.decode_content = True
        #        shutil.copyfileobj(rposter.raw, f0) 
        cmd = 'curl %s -o %s' % (self.poster_url, poster_path)
        print cmd
        subprocess.call([cmd], shell=True)
        print "poster saved."
        #self.fanart_url = response.xpath(fanart_url_XPath).extract_first()
        #print "Fanart url --> %s" % self.fanart_url
        #rfanart = requests.get(self.fanart_url, stream=True)
        #fanart_path = self.fid + "-fanart.jpg"
        #if rfanart.status_code == 200:
        #    with open(os.path.join('alldone/',fanart_path), 'wb') as f0:
        #        rfanart.raw.decode_content = True
        #        shutil.copyfileobj(rfanart.raw, f0) 
        #self.movie_desc = response.xpath(desc_XPath).extract_first()
        #print "Desc ---> %s" % self.movie_desc.encode('utf-8')

        actor = movie_item.select('/div/div/div/span/a/text()')      
        self.actors = actorTemplate%{'movie_star': actor, 'movie_star_photo': self.movie_star_photo}
        print "Actor --> %s" %self.actors.encode('utf-8')

        print "Date --> %s" % self.movie_date
       
        nfoInfo = nfoTemplate%{'movie_title': self.movie_title,'movie_desc': self.movie_desc, 'movie_rate': "",
            'movie_date': self.movie_date, 'mid': self.movie_id, 'actors': self.actors, 'studio': "", 'poster': self.poster_url, 'fanart': self.fanart_url}
        with open(os.path.join('alldone/', self.fid +".nfo"), "w") as nfofile:
            nfofile.write(nfoInfo.encode('utf-8'))
        print "%s NFO/Poster/Fanart Saved." % self.fid

    def closed(self, reason):
        pass
