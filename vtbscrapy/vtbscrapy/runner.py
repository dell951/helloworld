from scrapy.cmdline import execute

try:
    # execute(
    #     [
    #         'scrapy',
    #         'crawl',
    #         'vtb',
    #         '-a',
    #         'studio=blacked',
    #         '-a',
    #         'title=stretching',
    #         '-o',
    #         'out.json'
    #     ]
    # )

   execute(
       [
           'scrapy',
           'crawl',
           'search',
           '-a',
           'studio=vixen',
           '-a',
           'queryKey=anya.olsen',
            '-a',
           'filedate=19.10.01',
           '-a',
           'showFullresult=True',
           '-o',
           'out.json'
       ]
   )

except SystemExit:
    pass