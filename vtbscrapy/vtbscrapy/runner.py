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
            'queryKey=bunny.love',
            '-a',
            'filedate=18.11.24',
            '-a',
            'showFullresult=True',
            '-o',
            'out.json'
        ]
    )
except SystemExit:
    pass