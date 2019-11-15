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

old_title_XPath = "//div[contains(@class,'player-caption')]//h1[contains(@class,'caption-title')]/a/text()"
old_stars_XPath = "//div[contains(@class,'player-caption')]//p//a/text()"
old_startsURL_XPath = "//div[contains(@class,'player-caption')]//p//a/@href"
old_rate_XPath = "//div[contains(@class,'player-caption')]//span[contains(@class,'totalrate')]/text()"
old_date_XPath = "//div[contains(@class,'player-description')]//span[contains(@class, 'info')]/text()"
old_desc_XPath = "//div[contains(@class,'player-description')]//span[contains(@class, 'moreless')]/text()"
old_fanart_XPath = "//div[contains(@class,'swiper-wrapper')]//a[contains(@class,'swiper-content-item')]/img/@src"
old_poster_XPath = "//div[contains(@class, 'player-img-wrap')]//img/@src"

class QuotesSpider(scrapy.Spider):
    name = 'vtb'
    studio = ''
    title = ''
    actors = ''
    movie_title = ''
    movie_rate = ''
    movie_desc = ''
    movie_date = ''
    poster_url = ''
    fanart_url = ''
    
    def __init__(self, studio, title, *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)
        self.studio = studio
        self.title = title

    
    def start_requests(self):
        urls = [
            'https://www.' + self.studio + '.com/' + self.title]
        for url in urls:
            print 'Proceeding %s' % url
            request = scrapy.Request(url = url, callback = self.parse_byJson)
            request.meta['dont_redirect'] = True
            yield request
            None
    
    def parse_byJson(self, response):
        json_text = re.search('window.__INITIAL_STATE__ = (.*)?;', response.text)
        if json_text:
            json_obj = json.loads(json_text.group(1))
            allvideos = json_obj['videos']
            movie_data = allvideos[len(allvideos) - 1]
            page_data = json_obj['page']['data']['/%s' % self.title]['data']
            self.movie_title = movie_data['title']
            print 'Movie Tile         - %s' % self.movie_title.encode('utf-8')
            self.movie_rate = movie_data['textRating']
            print 'Rate               - %s' % self.movie_rate
            self.movie_date = movie_data['releaseDateFormatted']
            print 'Release Date       - %s' % self.movie_date
            self.movie_desc = movie_data['title']
            print 'Description        - %s' % self.movie_desc.encode('utf-8')
            posters = movie_data['images']['poster']
            subprocess.call('mkdir -p alldone', shell = True)
            for poster in posters:
                if '320x362' in poster['name']:
                    self.poster_url = poster['highdpi']['2x']
                    print 'poster             - %s' % self.poster_url
                    rposter = requests.get(self.poster_url, stream = True)
                    poster_path = self.title + '-poster.jpg'
                    if rposter.status_code == 200:
                        with open(os.path.join('alldone', poster_path), 'wb') as f0:
                            rposter.raw.decode_content = True
                            shutil.copyfileobj(rposter.raw, f0)
                    
            fanart = page_data['pictureset'][0]
            self.fanart_url = fanart['main'][0]['src']
            print 'fanart             - %s' % self.fanart_url
            rfanart = requests.get(self.fanart_url, stream = True)
            fanart_path = self.title + '-fanart.jpg'
            if rfanart.status_code == 200:
                with open(os.path.join('alldone', fanart_path), 'wb') as f1:
                    rfanart.raw.decode_content = True
                    shutil.copyfileobj(rfanart.raw, f1)
            models = movie_data['modelsSlugged']
            for model in models:
                star_url = '/%s' % model['slugged']
                print 'star_url             - %s' % star_url
                star_page = response.urljoin(star_url)
                yield scrapy.Request(star_page, callback = self.parse_stars_by_json)
                None
            
        else:
            print "Somehow I didn't find the Json data[Movie]"

    
    def parse_stars_by_json(self, response):
        json_text = re.search('window.__INITIAL_STATE__ = (.*)?;', response.text)
        if json_text:
            json_obj = json.loads(json_text.group(1))
            star_data = json_obj['models'][0]
            star_name = star_data['description']
            star_photo_url = star_data['images']['profile'][0]['src']
            subprocess.call('mkdir -p alldone/.actors', shell = True)
            print 'star actor         - %s' % star_photo_url            
            #i = 0
            #while i < 3:
            #    try:                 
            #        rstar_photo = requests.get(star_photo_url, stream = True, timeout=20)
            #        star_photo_path = star_name.replace(' ', '_') + '.jpg'
            #        if rstar_photo.status_code == 200:
            #            with open(os.path.join('alldone/.actors', star_photo_path), 'wb') as f2:
            #                rstar_photo.raw.decode_content = True
            #                shutil.copyfileobj(rstar_photo.raw, f2)
            #    except Exception:
            #        print 'Fetching star photo timeout, try again...'
            #        i += 1            
            self.actors = self.actors + actorTemplate % {
                'movie_star': star_name,
                'movie_star_photo': star_photo_url }
        else:
            print "Somehow I didn't find the Json data [Star]"

    
    def closed(self, reason):
        if self.movie_title != '':
            nfoInfo = nfoTemplate % {
                'movie_title': self.movie_title,
                'movie_desc': self.movie_desc,
                'movie_rate': self.movie_rate,
                'movie_date': self.movie_date,
                'title': self.title,
                'actors': self.actors,
                'studio': self.studio,
                'poster': self.poster_url,
                'fanart': self.fanart_url }
            with open(os.path.join('alldone/', self.title + '.nfo'), 'w') as nfofile:
                nfofile.write(nfoInfo.encode('utf-8'))
            print '%s NFO Saved.' % self.title.encode('utf-8')
        else:
            print 'Do nothing.'