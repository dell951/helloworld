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
video_item_xpath = '//div[contains(@class,"main-content-videos")]//div[contains(@class,"row sides")]//div[contains(@class,"card-video")]'
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
    found = False

    def __init__(self, studio, queryKey, filedate="", showFullresult=False, *args, **kwargs):
        super(SearchLetsdoeit, self).__init__(*args, **kwargs)
        self.studio = studio
        self.queryKey = queryKey.replace(".","%20")
        if filedate != "":
            self.filedate="20%s"%filedate.replace(".","-")
        self.showFullresult = showFullresult
        #adate = datetime.datetime.strptime(targetDate, "%Y-%m-%d").date()
        #self.filedate = "%s %d, %s" % (adate.strftime("%B"), adate.day, adate.strftime("%Y"))
        self.baseUrl = 'https://' + self.studio + '.com/search.en.html?q='+ self.queryKey
        
    def start_requests(self):
        urls = [
            self.baseUrl
        ]

        for url in urls:
            #print url
            yield scrapy.Request(url=url, callback=self.parse_movies)

    def parse_movies(self, response):
        videoItem = response.xpath(video_item_xpath).extract()
        if len(videoItem) == 0:
            print "Nothing found"
            pass
        for theVideo in videoItem:
            matchesDate = re.findall(r'20\d\d-\d\d-\d\d', theVideo)
            for match in matchesDate:
                if match == self.filedate:
                    matchUrl_match = re.search(r'<a\sclass=\"fake\"\shref=\"(.*?)\">', theVideo)
                    if matchUrl_match:
                        matchUrl = matchUrl_match.group(1)
                        cmd = "./runscrapy.sh %s %s" %(self.studio, matchUrl)
                        print "%s" % cmd
                        self.found = True
                    self.articleDict[match] = [self.count, match, matchUrl, cmd]
                    self.actionDict[self.count] = [cmd]
                    self.count += 1
            #yield scrapy.Request(theVideo, headers={"User-Agent": USER_AGENT}, callback=self.parse_date)

    def closed(self, reason):
        resultTable = Texttable()
        resultTable.set_cols_width([3, 20, 40, 80])
        isoDates = self.articleDict.keys()
        isoDates.sort(reverse=True)
        for isoDate in isoDates:
            resultTable.add_row(self.articleDict[isoDate])
        if self.showFullresult == True:
            print resultTable.draw()
        if self.found == False:
            print "Nothing found"
        #while True :   
        #    action_no = raw_input("Your choice: ")
        #    if action_no == '' :
        #        break
        #    else:
        #        print self.actionDict[int(action_no)][0]
