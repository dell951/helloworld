from scrapy.cmdline import execute

try:
    execute(
        [
            'scrapy',
            'crawl',
            'letsdoeit',
            '-a',
            'studio=letsdoeit',
            '-a',
            'title=babes-love-to-rock-n-roll',
            '-o',
            'out.json',
        ]
    )
except SystemExit:
    pass