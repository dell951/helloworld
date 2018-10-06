import scrapy
import os
import subprocess
import urlparse
import time
from texttable import Texttable

article_XPath = "//article[@class='videolist-item']"
date_XPath = ".//div[@class='videolist-caption-date']/text()"
title_XPath = ".//a/@href"

class SearchSpider(scrapy.Spider):
    name = "search"    
    studio = ""
    queryKey = ""
    baseUrl = ""
    articleDict = {}
    actionDict = {}
    count = 0

    def __init__(self, studio, queryKey, *args, **kwargs):
        super(SearchSpider, self).__init__(*args, **kwargs)
        self.studio = studio
        self.queryKey = queryKey.replace("."," ")
        self.baseUrl = 'https://www.' + self.studio + '.com/search?q='+ self.queryKey
       
    def start_requests(self):
        urls = [
            self.baseUrl
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        articles = response.xpath(article_XPath)        
        for article in articles:
            date = article.xpath(date_XPath).extract_first()
            isoDate = time.strftime('%Y-%m-%d', time.strptime(date, "%B %d, %Y"))
            title = article.xpath(title_XPath).extract_first()
            cmd = "./runscrapy.sh %s %s" %(self.studio, title.replace('/',''))
            self.articleDict[isoDate] = [self.count, date, title.replace('/',''), cmd]
            self.actionDict[self.count] = [cmd]
            self.count += 1

        nextPage_XPath = "//a[contains(@class,'pagination-link pagination-next ajaxable')]/@href"
        nextPageUrl = response.xpath(nextPage_XPath).extract_first()
        if nextPageUrl:
            yield scrapy.Request(urlparse.urljoin(self.baseUrl, nextPageUrl), callback=self.parse)

    def closed(self, reason):
        resultTable = Texttable()
        resultTable.set_cols_width([3, 20, 40, 80])
        isoDates = self.articleDict.keys() 
        isoDates.sort(reverse=True)
        for isoDate in isoDates:
            resultTable.add_row(self.articleDict[isoDate])
        print resultTable.draw()
        
        #while True :   
        #    action_no = raw_input("Your choice: ")
        #    if action_no == '' :
        #        break
        #    else:
        #        print self.actionDict[int(action_no)][0]
