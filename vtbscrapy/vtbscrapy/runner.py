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
           'queryKey=mia.split',
            '-a',
           'filedate=19.09.16',
           '-a',
           'showFullresult=True',
           '-o',
           'out.json'
       ]
   )

except SystemExit:
    pass