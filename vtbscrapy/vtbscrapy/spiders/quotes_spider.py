import scrapy
import requests
import shutil
import subprocess
import os
import codecs
import re
import json

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
  <id>%(title)s</id>
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

#for movie info
old_title_XPath = "//div[contains(@class,'player-caption')]//h1[contains(@class,'caption-title')]/a/text()"
old_stars_XPath =  "//div[contains(@class,'player-caption')]//p//a/text()"
old_startsURL_XPath = "//div[contains(@class,'player-caption')]//p//a/@href"
old_rate_XPath = "//div[contains(@class,'player-caption')]//span[contains(@class,'totalrate')]/text()"
old_date_XPath = "//div[contains(@class,'player-description')]//span[contains(@class, 'info')]/text()"
old_desc_XPath = "//div[contains(@class,'player-description')]//span[contains(@class, 'moreless')]/text()"
old_fanart_XPath = "//div[contains(@class,'swiper-wrapper')]//a[contains(@class,'swiper-content-item')]/img/@src"
old_poster_XPath = "//div[contains(@class, 'player-img-wrap')]//img/@src"

new_title_XPath = "//h1[@data-test-component='VideoTitle']/text()"
new_startsURL_XPath = "//div[@data-test-component='VideoModels']/a/@href"
new_rate_XPath = "//button[@data-test-component='RatingButton']//text()"
new_date_pattern = r'.*releaseDateFormatted":"(.* .* .*)","runLengthFormatted'
new_desc_pattern = r'.*"description":"(.*)","runLength":.*,"shootDate"'
# Fetch JSON object 
# https://jsoneditoronline.org/?id=bbef330441b24957aeaceedcea621ba7

class QuotesSpider(scrapy.Spider):
    name = "vtb"    
    studio = ""
    title = ""
    actors = ""
    movie_title = ""
    movie_rate = ""
    movie_desc = ""
    movie_date = ""
    poster_url = ""
    fanart_url = ""

    def __init__(self, studio, title, *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)
        self.studio = studio
        self.title = title

    def start_requests(self):
        urls = [
            'https://www.' + self.studio + '.com/'+ self.title
        ]
        for url in urls:
            print "Proceeding %s" % url
            request = scrapy.Request(url=url, callback=(self.parse_old if self.studio == "vixen" else self.parse_new))
            request.meta['dont_redirect'] = True
            yield request

    def parse_old(self, response):
        self.movie_title = response.xpath(old_title_XPath).extract_first()
        print "Movie Tile         - %s" % self.movie_title.encode('utf-8')
        #movie_stars = response.xpath(stars_XPath).extract()
        #print "Movie Stars    - %s" % movie_stars
        startURLs = response.xpath(old_startsURL_XPath).extract()
        print "Stars URL          - %s" % startURLs
        
        for starurl in startURLs:
            star_page = response.urljoin(starurl)
            yield scrapy.Request(star_page, callback=self.old_parse_stars)   

        self.movie_rate = response.xpath(old_rate_XPath).extract_first()
        print "Rate               - %s" % self.movie_rate
        self.movie_date = response.xpath(old_date_XPath).extract_first()
        print "Release Date       - %s" % self.movie_date
        self.movie_desc = response.xpath(old_desc_XPath).extract_first()
        print "Description        - %s" % self.movie_desc.encode('utf-8')
        
        self.poster_url = response.xpath(old_poster_XPath).extract_first()
        print "poster             - %s" % self.poster_url
        rposter = requests.get(self.poster_url, stream=True)
        poster_path = self.title + "-poster.jpg"
        if rposter.status_code == 200:
            with open(os.path.join('alldone',poster_path), 'wb') as f0:
                rposter.raw.decode_content = True
                shutil.copyfileobj(rposter.raw, f0) 

        self.fanart_url = response.xpath(old_fanart_XPath).extract_first()
        print "fanart             - %s" % self.fanart_url
        rfanart = requests.get(self.fanart_url, stream=True)
        fanart_path = self.title + "-fanart.jpg"
        if rfanart.status_code == 200:
            with open(os.path.join('alldone',fanart_path), 'wb') as f1:
                rfanart.raw.decode_content = True
                shutil.copyfileobj(rfanart.raw, f1) 
        
    def old_parse_stars(self, response):
        #for stars
        star_photo_XPath = "//div[contains(@class,'model-profile-thumb')]/img/@src"
        if self.studio.startswith("v"):
            star_name_XPath = "//td[contains(@class,'model-profile-info')]//h1[contains(@class,'caption-title')]/text()"
        else:
            star_name_XPath = "//div[contains(@class,'model-profile-info')]//h1[contains(@class,'caption-title')]/text()"

        subprocess.call("mkdir -p alldone/.actors", shell=True)  
        star_name = response.xpath(star_name_XPath).extract_first()
        star_photo_url = response.xpath(star_photo_XPath).extract_first()        
        print "star actor         - %s" % star_photo_url
        rstar_photo = requests.get(star_photo_url, stream=True)
        star_photo_path = star_name.replace(' ','_') + ".jpg"
        if rstar_photo.status_code == 200:
            with open(os.path.join('alldone/.actors',star_photo_path), 'wb') as f2:
                rstar_photo.raw.decode_content = True
                shutil.copyfileobj(rstar_photo.raw, f2) 
        
        self.actors = self.actors + actorTemplate%{'movie_star': star_name, 'movie_star_photo': star_photo_url}
        #print self.actors

    def parse_new(self, response):
        self.movie_title = response.xpath(new_title_XPath).extract_first()
        print "Movie Tile         - %s" % self.movie_title.encode('utf-8')
        startURLs = response.xpath(new_startsURL_XPath).extract()
        print "Stars URL          - %s" % startURLs
        self.movie_rate = response.xpath(new_rate_XPath).extract()[2]
        print "Rate               - %s" % self.movie_rate
        date_match = re.search(new_date_pattern, response.text)
        if date_match:
            self.movie_date = date_match.group(1)
        print "Release Date       - %s" % self.movie_date
        desc_match = re.search(new_desc_pattern, response.text)
        if desc_match:
            self.movie_desc = desc_match.group(1)
        print "Description        - %s" % self.movie_desc.encode('utf-8')

        json_text = re.search(r'window.__INITIAL_STATE__ = (.*)?;', response.text)
        if json_text:
            json_obj = json.loads(json_text.group(1))
            posters = json_obj["page"]["data"]["/%s"%self.title]["data"]["video"]["images"]['poster']
            for poster in posters:
                if '1920x1080' in poster["name"]:
                    print poster["src"]
                    self.poster_url = poster["src"]
                    print "poster             - %s" % self.poster_url
                    rposter = requests.get(self.poster_url, stream=True)
                    poster_path = self.title + "-poster.jpg"
                    if rposter.status_code == 200:
                        with open(os.path.join('alldone',poster_path), 'wb') as f0:
                            rposter.raw.decode_content = True
                            shutil.copyfileobj(rposter.raw, f0) 

            #only take the first as the fanart
            fanart = json_obj["page"]["data"]["/%s"%self.title]["data"]["pictureset"][0]
            self.fanart_url = fanart["main"][0]["src"]
            print "fanart             - %s" % self.fanart_url
            rfanart = requests.get(self.fanart_url, stream=True)
            fanart_path = self.title + "-fanart.jpg"
            if rfanart.status_code == 200:
                with open(os.path.join('alldone',fanart_path), 'wb') as f1:
                    rfanart.raw.decode_content = True
                    shutil.copyfileobj(rfanart.raw, f1)

            stars = json_obj["page"]["data"]["/%s"%self.title]["data"]["video"]["models"]
            for star in stars:
                self.actors = self.actors + actorTemplate%{'movie_star': star, 'movie_star_photo': ""}
        else:
            print "Somehow I didn't find the Json data"

    def closed(self, reason):
        if self.movie_title != '':
            nfoInfo = nfoTemplate%{'movie_title': self.movie_title,'movie_desc': self.movie_desc, 'movie_rate': self.movie_rate, 
                'movie_date': self.movie_date, 'title': self.title, 'actors': self.actors, 'studio': self.studio, 'poster': self.poster_url, 'fanart': self.fanart_url} 
            with open(os.path.join('alldone/',self.title+".nfo"), "w") as nfofile:
                nfofile.write(nfoInfo.encode('utf-8'))
            print "%s NFO Saved." % self.title.encode('utf-8')
        else:
            print "Do nothing."