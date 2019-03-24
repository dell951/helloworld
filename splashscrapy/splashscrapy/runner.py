from scrapy.cmdline import execute

try:
    execute(
        [
            'scrapy',
            'crawl',
            'searchbabes',
            '-a',
            'studio=babes',
            '-a',
            'queryKey=Gina.Valentina',
            '-a',
            'filedate=18.03.23',
            '-a',
            'showFullresult=True',
            '-o',
            'out.json'
        ]
    )
except SystemExit:
    pass