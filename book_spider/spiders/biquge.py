# -*- coding: utf-8 -*-

import scrapy
from urlparse import urljoin
from bs4 import BeautifulSoup
from book_spider.items import BookItem, ChapterItem
from book_spider.models import Book, Chapter, Category
from book_spider.utils import get_digit


class BiqugeSpider(scrapy.Spider):

    name = "biquge"
    allowed_domains = ["www.biquge.com", "www.biquku.com"]
    start_urls = (
        'http://www.biquku.com/xiaoshuodaquan/',
    )

    def parse(self, response):
        book_urls = set()
        body_unicode = response.body_as_unicode()
        soup = BeautifulSoup(body_unicode, 'lxml')
        book_tags = soup.select('#main .novellist ul li a')
        for book_tag in book_tags:

            book_href = book_tag.get('href')
            if book_href:
                yield scrapy.Request(book_href, callback=self.parse_book)

        # for url in book_urls:
        #     yield scrapy.Request(url, callback=self.parse_book)

    def parse_book(self, response):

        book_url = response.url
        soup = BeautifulSoup(response.body_as_unicode(), 'lxml')
        info_tag = soup.select('#maininfo #info')[0]
        title = info_tag.select('h1')[0].text

        author_tag = info_tag.select('p')[0]
        author = author_tag.text.encode('utf-8').split('：').pop()

        category_tag = soup.select('.box_con .con_top')[0]
        category_desc = category_tag.text
        category_name = category_desc.split('>')[1].strip()

        book_update_time_tag = info_tag.select('p')[2]
        book_update_time = book_update_time_tag.text.encode('utf-8').split('：').pop()

        info_tag = soup.select('#intro p')[0]
        info = info_tag.text

        avatar_tags = soup.select('#fmimg img')
        if avatar_tags:
            avatar_url = urljoin(book_url, avatar_tags[0].get('src'))
            avatar = avatar_url
        else:
            avatar = ''

        if len(soup.select('#fmimg .b')) > 0:
            status = 0
        else:
            status = 1

        category = Category.get_by_name(category_name)
        book = Book.get_by_title_and_author(title, author)

        chapter_tags = soup.select('.box_con #list dd a')

        if not book:
            book = Book.add(title, avatar, author, info, category.id, book_update_time, book_url, status)
            # new_chapter = None
            if len(chapter_tags) > 0:
                meta = {
                    'book_id': book.id,
                    'book_name': title,
                    'author': author,
                    'category_id': category.id,
                    'serial_num': 1,
                }
                first_chapter_url = '%s%s' % (book_url, chapter_tags[0].get('href'))
                yield scrapy.Request(first_chapter_url, meta=meta, callback=self.parse_chapter)
        else:
            if chapter_tags:
                newest_chapter_tag = chapter_tags[-1]
                newest_chapter_name = newest_chapter_tag.text
                exists_new_chapter = Chapter.get_newest_chapter_by_book(book.id)
                if not exists_new_chapter:
                    meta = {
                    'book_id': book.id,
                    'book_name': title,
                    'author': author,
                    'category_id': category.id,
                    'serial_num': 1,
                    }
                    first_chapter_url = '%s%s' % (book_url, chapter_tags[0].get('href'))
                    yield scrapy.Request(first_chapter_url, meta=meta, callback=self.parse_chapter)
                else:
                    if newest_chapter_name != exists_new_chapter:
                        new_chapter = exists_new_chapter

                        # if book.book_update_time.strftime('%Y-%m-%d') != book_update_time:
                        Book.update(title, avatar, author, info, category.id, book_update_time, book_url, status)
                        meta = {
                            'book_id': book.id,
                            'book_name': title,
                            'author': author,
                            'serial_num': new_chapter.serial_num,
                            'category_id': category.id,
                        }
                        yield scrapy.Request(new_chapter.crawl_url, meta=meta, callback=self.parse_chapter)
                        # new_chapter = Chapter.get_newest_chapter_by_book(book.id)


        # if not new_chapter:
        #     if len(chapter_tags) > 0:
        #         meta = {
        #             'book_id': book.id,
        #             'book_name': title,
        #             'author': author,
        #             'category_id': category.id,
        #             'serial_num': 1,
        #         }
        #         first_chapter_url = '%s%s' % (book_url, chapter_tags[0].get('href'))
        #         yield scrapy.Request(first_chapter_url, meta=meta, callback=self.parse_chapter)
        # else:
        #     meta = {
        #         'book_id': book.id,
        #         'book_name': title,
        #         'author': author,
        #         'serial_num': new_chapter.serial_num,
        #         'category_id': category.id,
        #     }
        #     yield scrapy.Request(new_chapter.crawl_url, meta=meta, callback=self.parse_chapter)


    def parse_chapter(self, response):

        chapter_url = response.url
        serial_num = int(response.meta.get('serial_num'))
        book_id = int(response.meta.get('book_id'))
        book_name = response.meta.get('book_name')
        author = response.meta.get('author')
        category_id = int(response.meta.get('category_id'))
        chapter_item = ChapterItem()
        soup = BeautifulSoup(response.body_as_unicode(), 'lxml')
        chapter_name_tag = soup.select('.bookname h1')[0]
        chapter_name = chapter_name_tag.text

        content = soup.select('#content')[0].text

        chapter_item['title'] = chapter_name
        chapter_item['content'] = content
        chapter_item['book_id'] = book_id
        chapter_item['book_name'] = book_name
        chapter_item['author'] = author
        chapter_item['serial_num'] = serial_num
        chapter_item['crawl_url'] = chapter_url
        chapter_item['category_id'] = category_id

        yield chapter_item

        next_chapter_tags = soup.select('.bottem1 a')
        if next_chapter_tags:
            next_chapter_tag = next_chapter_tags[3]

            next_chapter_url = next_chapter_tag.get('href')
            if next_chapter_url != 'index.html' and not next_chapter_url.startswith('../'):
                chapter_url = urljoin(response.url, next_chapter_url)
                meta = {
                    'book_id': book_id,
                    'book_name': book_name,
                    'author': author,
                    'serial_num': serial_num + 1,
                    'category_id': category_id,
                }
                yield scrapy.Request(chapter_url, meta=meta, callback=self.parse_chapter)