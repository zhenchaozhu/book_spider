# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CategoryItem(scrapy.Item):

    name = scrapy.Field()


class BookItem(scrapy.Item):

    avatar = scrapy.Field()
    title = scrapy.Field()
    info = scrapy.Field()
    author = scrapy.Field()
    category = scrapy.Field()
    status = scrapy.Field()
    book_update_time = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()


class ChapterItem(scrapy.Item):

    title = scrapy.Field()
    book_id = scrapy.Field()
    book_name = scrapy.Field()
    author = scrapy.Field()
    category_id = scrapy.Field()
    serial_num = scrapy.Field()
    content = scrapy.Field()
    crawl_url = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()


class BookSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
