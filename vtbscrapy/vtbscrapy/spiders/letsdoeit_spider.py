import scrapy
import requests
import shutil
import subprocess
import os
import codecs
import re
import json
import time

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

#https://letsdoeit.com/videos?keywords=babes-love-to-rock-n-roll

letsdoeit_Json_xpath = "//script[contains(@type,'application/ld+json')]/text()"

class LetsDoeItSpider(scrapy.Spider):
    name = "letsdoeit"    
    studio = ""
    title = ""
    actors = ""
    movie_title = ""
    movie_rate = ""
    movie_desc = ""
    movie_date = ""
    poster_url = ""
    fanart_url = ""
    base_url = ""

    def __init__(self, studio, title, *args, **kwargs):
        super(LetsDoeItSpider, self).__init__(*args, **kwargs)
        self.studio = studio
        self.title = title
        self.base_url = 'https://www.' + self.studio + '.com'

    def start_requests(self):
        search_url = self.base_url + '/videos?keywords=' + self.title
        print "Proceeding %s" % search_url 
        request = scrapy.Request(url=search_url, callback=self.search_letsdoeit)
#        request.meta['dont_redirect'] = True
        yield request

    def search_letsdoeit(self, response):
        movie_url_xpath="//div[contains(@class,'video-item')]//a[contains(@class,'item-top')]/@href"
        moive_urls = response.xpath(movie_url_xpath).extract()
        for movie_url in moive_urls:
            url = movie_url.rsplit('/', 1)[-1]
            if url == self.title:
                full_movie_url = self.base_url + movie_url
                request = scrapy.Request(url=full_movie_url, callback=self.parse_letsdoeit)
#                request.meta['dont_redirect'] = True
                yield request

    def parse_letsdoeit(self, response):
        json_text = response.xpath(letsdoeit_Json_xpath).extract_first()
        if json_text:
            formated_json = json_text.replace('\n','').replace('},    }','}}')
            movie_data = json.loads(formated_json)

            self.movie_title = movie_data["name"]
            print "Movie Tile         - %s" % self.movie_title.encode('utf-8')
            self.movie_rate = ''
            print "Rate               - %s" % self.movie_rate
            movie_simpledate = re.sub(r'T\d\d:\d\d:\d\d','',movie_data["uploadDate"]) #movie_data["uploadDate"].replace('T00:00:00','')
            self.movie_date = time.strftime('%B %d, %Y', time.strptime(movie_simpledate, "%Y-%m-%d"))
            print "Release Date       - %s" % self.movie_date
            self.movie_desc = movie_data["description"]
            print "Description        - %s" % self.movie_desc.encode('utf-8')

            #movie_data["thumbnailUrl"] 
            with open("tmp_response.txt", 'w') as html_file:
                html_file.write(response.text.encode('utf-8'))
            yield {
                'url': response.url
            }
            self.poster_url = response.xpath('//div[contains(@class,"owl-carousel")]//img[contains(@class,"owl-lazy")]/@data-src').extract()[1]
            print len(self.poster_url)
            print "poster             - %s" % self.poster_url
            rposter = requests.get(self.poster_url, stream=True)
            poster_path = self.title + "-poster.jpg"
            if rposter.status_code == 200:
                with open(os.path.join('alldone',poster_path), 'wb') as f0:
                    rposter.raw.decode_content = True
                    shutil.copyfileobj(rposter.raw, f0) 

            self.fanart_url = movie_data["thumbnailUrl"]
            print "fanart             - %s" % self.fanart_url
            rfanart = requests.get(self.fanart_url, stream=True)
            fanart_path = self.title + "-fanart.jpg"
            if rfanart.status_code == 200:
                with open(os.path.join('alldone',fanart_path), 'wb') as f1:
                    rfanart.raw.decode_content = True
                    shutil.copyfileobj(rfanart.raw, f1)

            star_urls = response.xpath('//h1[contains(@class,"big-container-title")]/../a[contains(@class,"pornstar")]/@href').extract()
            for star_url in star_urls:
                print "star_url             - %s" % star_url
                star_page = self.base_url + star_url
                yield scrapy.Request(star_page, callback=self.parse_stars_letsdoeit)

        else:
            print "Somehow I didn't find the Json data[Movie]"

    def parse_stars_letsdoeit(self, response):
        star_name = response.xpath('//h1/text()').extract_first().rstrip().lstrip()
        star_photo_url = response.xpath('//div[contains(@class,"pornstar-cover")]/div/img/@src').extract_first()
        subprocess.call("mkdir -p alldone/.actors", shell=True)  
        print "star actor         - %s" % star_photo_url
        rstar_photo = requests.get(star_photo_url, stream=True)
        star_photo_path = star_name.replace(' ','_') + ".jpg"
        if rstar_photo.status_code == 200:
            with open(os.path.join('alldone/.actors',star_photo_path), 'wb') as f2:
                rstar_photo.raw.decode_content = True
                shutil.copyfileobj(rstar_photo.raw, f2) 
            self.actors = self.actors + actorTemplate%{'movie_star': star_name, 'movie_star_photo': star_photo_url}
        else:
            print "Somehow I didn't find the Json data [Star]"

    def closed(self, reason):
        if self.movie_title != '':
            nfoInfo = nfoTemplate%{'movie_title': self.movie_title,'movie_desc': self.movie_desc, 'movie_rate': self.movie_rate, 
                'movie_date': self.movie_date, 'title': self.title, 'actors': self.actors, 'studio': self.studio, 'poster': self.poster_url, 'fanart': self.fanart_url} 
            with open(os.path.join('alldone/',self.title+".nfo"), "w") as nfofile:
                nfofile.write(nfoInfo.encode('utf-8'))
            print "%s NFO Saved." % self.title.encode('utf-8')
        else:
            print "Do nothing."