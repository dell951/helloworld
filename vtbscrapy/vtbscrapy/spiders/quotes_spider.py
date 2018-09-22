import scrapy
import requests
import shutil
import subprocess
import os
import codecs

nfoTemplate = """
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
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
  <thumb></thumb>
  <fanart>
    <thumb></thumb>
  </fanart>
  <mpaa></mpaa>
  <id>%(title)s</id>
  <genre></genre>
  %(actors)s
  <director></director>
</movie>
"""

actorTemplate = """
  <actor>
    <name>%(movie_star)s</name>
    <role></role>
    <thumb></thumb>
  </actor>
"""

#for movie info
title_XPath = "//div[contains(@class,'player-caption')]//h1[contains(@class,'caption-title')]/a/text()"
stars_XPath =  "//div[contains(@class,'player-caption')]//p//a/text()"
startsURL_XPath = "//div[contains(@class,'player-caption')]//p//a/@href"
rate_XPath = "//div[contains(@class,'player-caption')]//span[contains(@class,'totalrate')]/text()"
date_XPath = "//div[contains(@class,'player-description')]//span[contains(@class, 'info')]/text()"
desc_XPath = "//div[contains(@class,'player-description')]//span[contains(@class, 'moreless')]/text()"
fanart_XPath = "//div[contains(@class, 'player-img-wrap')]//img/@src"
poster_XPath = "//div[contains(@class,'swiper-wrapper')]//a[contains(@class,'swiper-content-item')]/img/@src"



class QuotesSpider(scrapy.Spider):
    name = "vtb"    
    studio = ""
    title = ""

    def __init__(self, studio, title, *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)
        self.studio = studio
        self.title = title

    def start_requests(self):
        urls = [
            'https://www.' + self.studio + '.com/'+ self.title
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        movie_title = response.xpath(title_XPath).extract_first()
        print "Movie Tile     - %s" % movie_title
        movie_stars = response.xpath(stars_XPath).extract()
        print "Movie Stars    - %s" % movie_stars
        actors = ""
        for star in movie_stars:
            if actors == "":
                actors = actorTemplate%{'movie_star': star}
            else:
                actors = actors + actorTemplate%{'movie_star': star}

        startURLs = response.xpath(startsURL_XPath).extract()
        print "Stars URL      - %s" % startURLs
        movie_rate = response.xpath(rate_XPath).extract_first()
        print "Rate           - %s" % movie_rate
        movie_date = response.xpath(date_XPath).extract_first()
        print "Release Date   - %s" % movie_date
        movie_desc = response.xpath(desc_XPath).extract_first()
        print "Description    - %s" % movie_desc
        poster_url = response.xpath(poster_XPath).extract_first()
        print "poster         - %s" % poster_url
        rposter = requests.get(poster_url, stream=True)
        poster_path = self.title + "-fanart.jpg"
        if rposter.status_code == 200:
            with open(os.path.join('alldone',poster_path), 'wb') as f0:
                rposter.raw.decode_content = True
                shutil.copyfileobj(rposter.raw, f0) 

        fanart_url = response.xpath(fanart_XPath).extract_first()
        print "fanart         - %s" % fanart_url
        rfanart = requests.get(fanart_url, stream=True)
        fanart_path = self.title + "-poster.jpg"
        if rfanart.status_code == 200:
            with open(os.path.join('alldone',fanart_path), 'wb') as f1:
                rfanart.raw.decode_content = True
                shutil.copyfileobj(rfanart.raw, f1) 
        
        for href in startURLs:
            star_page = response.urljoin(href)
            yield scrapy.Request(star_page, callback=self.parse_stars)

        nfoInfo = nfoTemplate%{'movie_title': movie_title,'movie_desc': movie_desc, 'movie_rate': movie_rate, 'movie_date': movie_date, 'title': self.title, 'actors': actors, 'studio': self.studio} 
        with open(os.path.join('alldone/',self.title+".nfo"), "w") as nfofile:
            nfofile.write(nfoInfo.encode('utf-8'))

    def parse_stars(self, response):
        #for stars
        star_photo_XPath = "//div[contains(@class,'model-profile-thumb')]/img/@src"
        if self.studio == "vixen":
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