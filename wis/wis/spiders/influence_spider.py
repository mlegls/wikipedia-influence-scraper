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
        Rule(LinkExtractor(allow=rf'(?!{"|".join(g.processed)})',  # reduces returning to already-processed urls
                           restrict_xpaths=['//*[text()="Influences"]/following-sibling::ul//a[@title]',
                                            '//*[text()="Influenced"]/following-sibling::ul//a[@title]']),
             callback="parse_thinker",
             follow=True),
    )

    def parse_start_url(self, response):
        g.thinkers = []
        g.processed = ['filler']
        return self.parse_thinker(response)

    def parse_thinker(self, response):
        link = response.request.url

        # regex removes parentheticals like '(philosopher)'
        name = response.xpath('//h1/text()').re(r'^(?:(?! \().)*')[0]

        # main process
        if link in g.processed:
            print('Already been ' + str(g.processed))
            return
        else:
            g.processed.append(link)

            thinker = Thinker()

            thinker['name'] = name
            thinker['link'] = link
            thinker['influences'] = []
            thinker['influenced'] = []

            g.full_graph.add_node(name)

            # add influences; ul = collapsible, td = non-collapsible
            # r'^(?:(?! \().)*' removes parentheticals like '(philosopher)' or '(no page)'
            for t in response.xpath('//*[text()="Influences"]/following-sibling::ul//a/@title').re(r'^(?:(?! \().)*') \
                     + response.xpath('//*[text()="Influences"]/following-sibling::td//a/@title').re(r'^(?:(?! \().)*'):
                # for scrapy Thinker object
                thinker['influences'].append(t)
                # edge from influences to this
                g.full_graph.add_edge(t, name)

            # add influenced
            for t in response.xpath('//*[text()="Influenced"]/following-sibling::ul//a/@title').re(r'^(?:(?! \().)*') \
                     + response.xpath('//*[text()="Influenced"]/following-sibling::td//a/@title').re(r'^(?:(?! \().)*'):
                # for scrapy Thinker object
                thinker['influenced'].append(t)
                # edge from this to influenced
                g.full_graph.add_edge(name, t)

            # update thinker list
            g.thinkers.append(thinker)
            return thinker
