from scrapy.cmdline import execute

try:
    execute(
        [
            'scrapy',
            'crawl',
            'vtb',
            '-a',
            'studio=tushy',
            '-a',
            'title=one-last-time',
            '-o',
            'out.json'
        ]
    )

    #    execute(
#        [
#            'scrapy',
#            'crawl',
#            'searchletsdoeit',
#            '-a',
#            'studio=letsdoeit',
#            '-a',
#            'queryKey=stacy.cruz',
#            '-a',
#            'filedate=19.06.06',
#            '-a',
#            'showFullresult=True',
#            '-o',
#            'out.json'
#        ]
#    )
except SystemExit:
    pass