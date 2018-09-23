import scrapy

article_XPath = "//article[@class='videolist-item']"
date_XPath = ".//div[@class='videolist-caption-date']/text()"
title_XPath = ".//a/@href"

class SearchSpider(scrapy.Spider):
    name = "search"    
    studio = ""
    queryKey = ""

    def __init__(self, studio, queryKey, *args, **kwargs):
        super(SearchSpider, self).__init__(*args, **kwargs)
        self.studio = studio
        self.queryKey = queryKey.replace("."," ")

    def start_requests(self):
        urls = [
            'https://www.' + self.studio + '.com/search?q='+ self.queryKey
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        articles = response.xpath(article_XPath)
        #print articles[0]
        for article in articles:
            #print article
            date = article.xpath(date_XPath).extract_first()
            title = article.xpath(title_XPath).extract_first()
            #print "%s ---- %s" % (title.replace('/',''), date)
            print "%s ./runscrapy.sh %s %s" %(date ,self.studio, title.replace('/',''))