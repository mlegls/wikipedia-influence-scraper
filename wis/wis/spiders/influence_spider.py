"""main spider; logic is in here"""

import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from .. import globfile as g
from ..items import Thinker


# main spider
class InfluenceSpider(CrawlSpider):
    name = 'influence'
    allowed_domains = ['en.wikipedia.org']

    rules = (
        Rule(LinkExtractor(allow=rf'(?!{"|".join(g.processed)})',  # prevents returning to already-processed urls
                           restrict_xpaths=['//*[text()="Influences"]/following-sibling::ul//a[@title]',
                                            '//*[text()="Influenced"]/following-sibling::ul//a[@title]']),
             callback="parse_thinker",
             follow=True),
    )

    def parse_start_url(self, response):
        return self.parse_thinker(response)

    def parse_thinker(self, response):

        # regex removes parentheticals like '(philosopher)'
        this_name = response.xpath('//h1/text()').re(r'^(?:(?! \().)*')[0]
        link = response.request.url

        g.processed.append(link)

        # main process
        thinker = Thinker()

        thinker['name'] = this_name
        thinker['link'] = link
        thinker['influences'] = []
        thinker['influenced'] = []

        g.full_graph.add_node(this_name)

        # add influences
        for t in response.xpath('//*[text()="Influences"]/following-sibling::ul//a'):
            name = t.re(r'title="(.*)"')
            if name:
                next_name = re.match(r'^(?:(?! \().)*', name[0])  # regex removes parentheticals like '(philosopher)'
                thinker['influences'].append(name[0])
                # edge from influences to this
                g.full_graph.add_edge(next_name, this_name)

        # add influenced
        for t in response.xpath('//*[text()="Influenced"]/following-sibling::ul//a'):
            name = t.re(r'title="(.*)"')
            if name:
                next_name = re.match(r'^(?:(?! \().)*', name[0])  # regex removes parentheticals like '(philosopher)'
                thinker['influenced'].append(name[0])
                # edge from this to influenced
                g.full_graph.add_edge(this_name, next_name)

        # update thinker list
        g.thinkers.append(thinker)
        return thinker
