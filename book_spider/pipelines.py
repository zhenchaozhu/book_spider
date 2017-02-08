# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
from book_spider import settings
# from config import db_session
from book_spider.models import Book, Chapter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ChapterPipeline(object):

    def __init__(self):

        DB_CONNECT_STRING = 'mysql+mysqldb://root:root@127.0.0.1/mybook?charset=utf8'
        self.engine = create_engine(DB_CONNECT_STRING)
        self.db_session = sessionmaker(bind=self.engine)

    def process_item(self, item, spider):

        title = item.get('title')
        book_id = item.get('book_id')
        content = item.get('content')
        serial_num = item.get('serial_num')
        crawl_url = item.get('crawl_url')
        category_id = item.get('category_id')
        chapter = Chapter.get_by_serial_num_and_book(serial_num, book_id)
        if not chapter:
            chapter_path = os.path.join(settings.BOOK_DIR, str(book_id))
            if not os.path.exists(chapter_path):
                os.makedirs(chapter_path)
            # if not os.path.exists(chapter_a )
            chapter_file = os.path.join(chapter_path, '%s.txt' % serial_num)
            with open(chapter_file, 'w+') as f:
                f.write(content)
            session = self.db_session()
            chapter = Chapter.add(session, title, book_id, category_id, serial_num, chapter_file, crawl_url)
            session.close()


class BookSpiderPipeline(object):
    def process_item(self, item, spider):
        return item
