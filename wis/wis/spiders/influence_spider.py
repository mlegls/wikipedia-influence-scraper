from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import Thinker

thinkers = []
processed = ['filler']


# main spider
class InfluenceSpider(CrawlSpider):
    name = 'influence'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Gilles_Deleuze']

    rules = (
        Rule(LinkExtractor(allow=rf'(?!{"|".join(processed)})',
                           restrict_xpaths=['//*[text()="Influences"]/following-sibling::ul//a[@title]',
                                            '//*[text()="Influenced"]/following-sibling::ul//a[@title]']),
             callback="parse_thinker",
             follow=True),
    )

    def parse_thinker(self, response):

        name = response.xpath('//h1/text()').get()
        link = response.request.url

        processed.append(link)

        # main process
        thinker = Thinker()

        thinker['name'] = name
        thinker['link'] = link
        thinker['influences'] = []
        thinker['influenced'] = []

        # add influences
        for t in response.xpath('//*[text()="Influences"]/following-sibling::ul//a'):
            name = t.re(r'title="(.*)"')
            thinker['influences'].append(name[0])

        # add influenced
        for t in response.xpath('//*[text()="Influenced"]/following-sibling::ul//a'):
            name = t.re(r'title="(.*)"')
            thinker['influenced'].append(name[0])

        # update thinker list
        thinkers.append(thinker)
        return thinker
