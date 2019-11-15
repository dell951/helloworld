import scrapy
import os
import subprocess
import urlparse
from datetime import datetime, timedelta
import time
import re
from texttable import Texttable
import json

#format file with regex:
#(vixen|tushy)\s(\d\d\.\d\d\.\d\d)\.(.*)(\.And.*)?\.XXX.*

old_article_XPath = "//article[@class='videolist-item']"
old_date_XPath = ".//div[@class='videolist-caption-date']/text()"
old_title_XPath = ".//a/@href"

new_article_XPath = "//div[contains(@data-test-component,'VideoList')]//div[@data-test-component='VideoThumbnailContainer']/div/a/@href"
new_date_XPath = "//button[@data-test-component='ReleaseDate']/span/text()"
#new_title_XPath = "//h1[@data-test-component='VideoTitle']/text()"
new_date_pattern = r'.*releaseDateFormatted\":\"(.*\s.*,\s201\d)\"\}\]'
#new_date_pattern = r'<span data-test-component=\"ReleaseDateFormatted\">(.*\s.*,\s201\d)</span>'

class SearchSpider(scrapy.Spider):
    name = "search"    
    studio = ""
    queryKey = ""
    filedate = ""
    baseUrl = ""
    articleDict = {}
    actionDict = {}
    count = 0
    showFullresult = False

    def __init__(self, studio, queryKey, filedate="", showFullresult=False, *args, **kwargs):
        super(SearchSpider, self).__init__(*args, **kwargs)
        self.studio = studio
        self.queryKey = queryKey.replace(".","-")
        if filedate != "":
            self.filedate="20%s"%filedate.replace(".","-")
        self.showFullresult = showFullresult
        #adate = datetime.datetime.strptime(targetDate, "%Y-%m-%d").date()
        #self.filedate = "%s %d, %s" % (adate.strftime("%B"), adate.day, adate.strftime("%Y"))
        self.baseUrl = 'https://www.' + self.studio + '.com/'+ self.queryKey
       
    def start_requests(self):
        urls = [
            self.baseUrl
        ]

        for url in urls:
            print url
            yield scrapy.Request(url=url, callback=(self.parse_new))

    def parse_old(self, response):
        #print "handle vixen"
        articles = response.xpath(old_article_XPath)
        if len(articles) == 0:
            print "Nothing found"
            pass
        for article in articles:
            date = article.xpath(old_date_XPath).extract_first()
            #print date
            isoDate = time.strftime('%Y-%m-%d', time.strptime(date, "%B %d, %Y"))
            title = article.xpath(old_title_XPath).extract_first()
            cmd = "./runscrapy.sh %s %s" %(self.studio, title.replace('/',''))
            if isoDate == self.filedate:
                print "%s" % cmd
            self.articleDict[isoDate] = [self.count, date, title.replace('/',''), cmd]
            self.actionDict[self.count] = [cmd]
            self.count += 1

        nextPage_XPath = "//a[contains(@class,'pagination-link pagination-next ajaxable')]/@href"
        nextPageUrl = response.xpath(nextPage_XPath).extract_first()
        if nextPageUrl:
            yield scrapy.Request(urlparse.urljoin(self.baseUrl, nextPageUrl), callback=self.parse)

    def parse_new(self, response):
        #print "handle tushy/blacked"
        articles = response.xpath(new_article_XPath).extract()
        if len(articles) == 0:
            print "Nothing found"
            pass
        for article in articles:
            movie_url = response.urljoin(article)
            print movie_url
            yield scrapy.Request(movie_url, callback=self.parse_date_by_json)

        #nextPage_XPath = "//a[contains(@class,'pagination-link pagination-next ajaxable')]/@href"
        #nextPageUrl = response.xpath(nextPage_XPath).extract_first()
        #if nextPageUrl:
        #    yield scrapy.Request(urlparse.urljoin(self.baseUrl, nextPageUrl), callback=self.parse)

    def parse_date(self, response):
        #print response.text
        #with open("tmp_response.txt", 'w') as html_file:
        #    html_file.write(response.text)
        #yield {
        #    'url': response.url
        #}
        #print use regex here to parse the date, or otherwise go with splash.... 
        
        date_match = re.search(new_date_pattern, response.text)
        if date_match:
            date = date_match.group(1)
            realDate = datetime.strptime(date,"%B %d, %Y") + timedelta(days=1)
            isoDate = realDate.strftime('%Y-%m-%d') 
            cmd = "./runscrapy.sh %s %s" %(self.studio, response.url.replace('https://www.' + self.studio + '.com/', ''))
            #print isoDate + ' ' + cmd
            if isoDate == self.filedate:
                print "%s" % cmd
            self.articleDict[isoDate] = [self.count, date, response.url.replace('https://www.' + self.studio + '.com/', ''), cmd]
            self.actionDict[self.count] = [cmd]
            self.count += 1

        else:
            print "No date found."

    def parse_date_by_json(self, response):
        json_text = re.search('window.__INITIAL_STATE__ = (.*)?;', response.text)
        if json_text:
            json_obj_txt = json_text.group(1)
            json_obj = json.loads(json_obj_txt)
            allMovies = json_obj["videos"]
            for movie in allMovies:
                if "id" in movie:
                    date = movie["releaseDateFormatted"]
                    realDate = datetime.strptime(date,"%B %d, %Y")# + timedelta(days=1)
                    isoDate = realDate.strftime('%Y-%m-%d') 
                    cmd = "./runscrapy.sh %s %s" %(self.studio, response.url.replace('https://www.' + self.studio + '.com/', ''))
                    #print isoDate + ' ' + cmd
                    if isoDate == self.filedate:
                        print "%s" % cmd
                    self.articleDict[isoDate] = [self.count, date, response.url.replace('https://www.' + self.studio + '.com/', ''), cmd]
                    self.actionDict[self.count] = [cmd]
                    self.count += 1
            #print json_obj

    def closed(self, reason):
        resultTable = Texttable()
        resultTable.set_cols_width([3, 20, 40, 80])
        isoDates = self.articleDict.keys() 
        isoDates.sort(reverse=True)
        for isoDate in isoDates:
            resultTable.add_row(self.articleDict[isoDate])
        if self.showFullresult == True:
            print resultTable.draw()
        
        #while True :   
        #    action_no = raw_input("Your choice: ")
        #    if action_no == '' :
        #        break
        #    else:
        #        print self.actionDict[int(action_no)][0]
