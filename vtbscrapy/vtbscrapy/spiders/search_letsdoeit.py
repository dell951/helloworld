import scrapy
import os
import subprocess
import urlparse
import datetime
import time
import re
import json
from texttable import Texttable

#format file with regex:
#(vixen|tushy)\s(\d\d\.\d\d\.\d\d)\.(.*)(\.And.*)?\.XXX.*

USER_AGENT = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
video_item_xpath = '//div[contains(@class,"row")]//div[contains(@class,"video-item")]//a[contains(@class,"title")]/@href'
letsdoeit_Json_xpath = "//script[contains(@type,'application/ld+json')]/text()"
target_url_pattern = r'trailer\/.*?\/(.*)'

class SearchLetsdoeit(scrapy.Spider):
    name = "searchletsdoeit"    
    studio = ""
    queryKey = ""
    filedate = ""
    baseUrl = ""
    articleDict = {}
    actionDict = {}
    count = 0
    showFullresult = False

    def __init__(self, studio, queryKey, filedate="", showFullresult=False, *args, **kwargs):
        super(SearchLetsdoeit, self).__init__(*args, **kwargs)
        self.studio = studio
        self.queryKey = queryKey
        if filedate != "":
            self.filedate="20%s"%filedate.replace(".","-")
        self.showFullresult = showFullresult
        #adate = datetime.datetime.strptime(targetDate, "%Y-%m-%d").date()
        #self.filedate = "%s %d, %s" % (adate.strftime("%B"), adate.day, adate.strftime("%Y"))
        self.baseUrl = 'https://' + self.studio + '.com/videos?keywords='+ self.queryKey
        
    def start_requests(self):
        urls = [
            self.baseUrl
        ]

        for url in urls:
            #print url
            yield scrapy.Request(url=url, callback=self.parse_movies)

    def parse_movies(self, response):
        articles = response.xpath(video_item_xpath).extract()
        if len(articles) == 0:
            print "Nothing found"
            pass
        for article in articles:
            movie_url = 'https://www.' + self.studio + '.com' + article
            #print movie_url
            yield scrapy.Request(movie_url, headers={"User-Agent": USER_AGENT}, callback=self.parse_date)

    def parse_date(self, response):
        json_text = response.xpath(letsdoeit_Json_xpath).extract_first()
        if json_text:
            formated_json = json_text.replace('\n','').replace('},    }','}}')
            movie_data = json.loads(formated_json)
            movie_simpledate = re.sub(r'T\d\d:\d\d:\d\d','',movie_data["uploadDate"]) #movie_data["uploadDate"].replace('T00:00:00','')
            movie_id = movie_data['url'].replace('https://' + self.studio + '.com/video/', '')
            movie_id = movie_id.split('/')[1]
            #isoDate = time.strftime('%Y-%m-%d', time.strptime(movie_simpledate, "%B %d, %Y"))
            cmd = "./runscrapy.sh %s %s" %(self.studio, movie_id)
            #print isoDate + ' ' + cmd
            if movie_simpledate == self.filedate:
                print "%s" % cmd

            self.articleDict[movie_simpledate] = [self.count, movie_simpledate, movie_id, cmd]
            self.actionDict[self.count] = [cmd]
            self.count += 1

        else:
            print "No date found."

    def closed(self, reason):
        resultTable = Texttable()
        resultTable.set_cols_width([3, 20, 40, 80])
        isoDates = self.articleDict.keys() 
        isoDates.sort(reverse=True)
        for isoDate in isoDates:
            resultTable.add_row(self.articleDict[isoDate])
        if self.showFullresult:
            print resultTable.draw()
        
        #while True :   
        #    action_no = raw_input("Your choice: ")
        #    if action_no == '' :
        #        break
        #    else:
        #        print self.actionDict[int(action_no)][0]
