from scrapy.cmdline import execute

try:
    execute(
        [
            'scrapy',
            'crawl',
            'vtb',
            '-a',
            'studio=blacked',
            '-a',
            'title=stretching',
            '-o',
            'out.json'
        ]
    )

#    execute(
#        [
#            'scrapy',
#            'crawl',
#            'search',
#            '-a',
#            'studio=tushy',
#            '-a',
#            'queryKey=stacy.cruz',
##            '-a',
#            'filedate=19.06.30',
#            '-a',
#            'showFullresult=True',
#            '-o',
#            'out.json'
#        ]
#    )

except SystemExit:
    pass