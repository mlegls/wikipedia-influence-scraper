# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


# core thinker object
"""thinker item; represents one Wikipedia page, unless no page"""
class Thinker(Item):
    name = Field()
    link = Field()

    # lists of names
    influences = Field()
    influenced = Field()
