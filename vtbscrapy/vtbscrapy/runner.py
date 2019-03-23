from scrapy.cmdline import execute

try:
    execute(
        [
            'scrapy',
            'crawl',
            'searchletsdoeit',
            '-a',
            'studio=letsdoeit',
            '-a',
            'queryKey=lovenia.lux',
            '-a',
            'filedate=19.03.16',
            '-a',
            'showFullresult=True',
            '-o',
            'out.json'
        ]
    )
except SystemExit:
    pass