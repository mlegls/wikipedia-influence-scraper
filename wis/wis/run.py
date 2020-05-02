"""networkx stuff, including UI"""

from wis.wis.spiders.influence_spider import InfluenceSpider
from scrapy.crawler import CrawlerProcess


def do_craw(url):
    # init crawler process, export json
    process = CrawlerProcess(settings={
        "FEEDS": {
            "thinkers.json": {"format": "json"},
        },
    })

    # create crawler with initial page at "url"
    process.crawl(InfluenceSpider, start_urls=[url])
    process.start()


do_craw('https://en.wikipedia.org/wiki/Gilles_Deleuze')
