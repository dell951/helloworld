from scrapy.cmdline import execute

try:
    #for letsdoeit
    execute(
        [
            'scrapy',
            'crawl',
            'letsdoeit',
            '-a',
            'studio=letsdoeit',
            '-a',
            'title=https://letsdoeit.com/watch/71876/anal-happy-ending.en.html',
            '-o',
            'out.json'
        ]
    )

    # for vtb
    # execute(
    #     [
    #         'scrapy',
    #         'crawl',
    #         'vtb',
    #         '-a',
    #         'studio=blacked',
    #         '-a',
    #         'title=best-friends-share',
    #         '-o',
    #         'out.json'
    #     ]
    # )

#    execute(
#        [
#            'scrapy',
#            'crawl',
#            'search',
#            '-a',
#            'studio=vixen',
#            '-a',
#            'queryKey=anya.olsen',
#             '-a',
#            'filedate=19.10.01',
#            '-a',
#            'showFullresult=True',
#            '-o',
#            'out.json'
#        ]
#    )

except SystemExit:
    pass