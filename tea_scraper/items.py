# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class TeaResearchItem(scrapy.Item):
    title = scrapy.Field()
    authors = scrapy.Field()  # 列表
    publication_date = scrapy.Field()
    abstract = scrapy.Field()
    url = scrapy.Field()