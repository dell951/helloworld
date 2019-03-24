import scrapy
import os
import subprocess
import urlparse
import datetime
import time
import re
import json
from texttable import Texttable
from scrapy.selector import HtmlXPathSelector
from scrapy_splash import SplashRequest

#format file with regex:
#(vixen|tushy)\s(\d\d\.\d\d\.\d\d)\.(.*)(\.And.*)?\.XXX.*

video_item_xpath = "//div[contains(@class,'GridItem')]//h1//a/@href"

class SearchBabes(scrapy.Spider):
    name = "searchbabes"    
    studio = ""
    queryKey = ""
    filedate = ""
    baseUrl = ""
    articleDict = {}
    actionDict = {}
    count = 0
    showFullresult = False
    found = False

    def __init__(self, studio, queryKey, filedate="", showFullresult=False, *args, **kwargs):
        super(SearchBabes, self).__init__(*args, **kwargs)
        self.studio = studio
        self.queryKey = queryKey
        if filedate != "":
            self.filedate="20%s"%filedate.replace(".","-")
        self.showFullresult = showFullresult
        self.baseUrl = 'https://www.' + self.studio + '.com/search?q='+ self.queryKey
        
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
            yield SplashRequest(url=url, callback=self.parse_movies, endpoint='execute', args={'wait': 5.5, 'lua_source':script})

    def parse_movies(self, response):
        hxs = HtmlXPathSelector(response)
        movie_items = hxs.select('//div[contains(@class,"GridItem")]')
        if len(movie_items) == 0:
            print "Nothing found"
            pass

        for movie in movie_items:
            movie_link = movie.select('.//h1/a/@href').extract_first()
            movie_date = movie.select('.//div[contains(@class,"-3")]/div[contains(@class,"-5")]/text()').extract_first()
            movie_id = movie_link.split('/')[3]
            isoDate = time.strftime('%Y-%m-%d', time.strptime(movie_date, "%b %d, %Y"))
            cmd = "./runscrapy.sh %s %s" %(self.studio, movie_link)
            if isoDate == self.filedate:
                print "%s" % cmd
                self.found = True

            self.articleDict[movie_date] = [self.count, movie_date, movie_id, cmd]
            self.actionDict[self.count] = [cmd]
            self.count += 1

    def closed(self, reason):
        resultTable = Texttable()
        resultTable.set_cols_width([3, 20, 40, 80])
        isoDates = self.articleDict.keys()
        isoDates.sort(reverse=True)
        for isoDate in isoDates:
            resultTable.add_row(self.articleDict[isoDate])
        if self.showFullresult == 'True':
            print resultTable.draw()
        if self.found == False:
            print "Nothing found"
