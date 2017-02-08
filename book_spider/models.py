# coding: utf-8

import qiniu
import hashlib
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Text, create_engine
from sqlalchemy.sql import func, exists
from sqlalchemy.ext.declarative import declarative_base
from config import db_session, DB_CONNECT_STRING
from qiniu import Auth
from qiniu import BucketManager

AK = 'AUV20tuE-G41IHIu04wZZPXxlJzaNnGNtYdeJeyM'
SK = 'Dw4Hscr74R_Qn_KXV5M3sxDsiMM-DYnkZx78j-hz'
bucket_name = 'star428'
BaseModel = declarative_base()
auth = Auth(AK, SK)
bucket = BucketManager(auth)


class Category(BaseModel):

    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    create_time = Column(DateTime, default=func.now())
    update_time = Column(DateTime, onupdate=datetime.now())

    @classmethod
    def get_by_name(cls, name):
        session = db_session()
        category = session.query(Category).filter_by(name=name).first()
        if not category:
            category = Category(name=name)
            session.add(category)
            try:
                session.commit()
            except:
                session.rollback()

        return category


class Book(BaseModel):

    __tablename__ = 'book'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50))
    avatar = Column(String(255))
    info = Column(Text)
    author = Column(String(50))
    category_id = Column(Integer)
    book_update_time = Column(DateTime)
    status = Column(Integer) # 0代表连载中,1代表已完本
    crawl_url = Column(String(255))
    create_time = Column(DateTime, default=func.now())
    update_time = Column(DateTime, onupdate=datetime.now())

    @classmethod
    def exists_book(cls, title, author):
        session = db_session()
        q = session.query(Book).filter_by(title = title, author = author)
        return session.query(q.exists())

    @classmethod
    def get_by_title_and_author(cls, title, author):
        session = db_session()
        book = session.query(Book).filter(Book.title == title,
                                             Book.author == author).scalar()
        return book

    @classmethod
    def add(cls, title, avatar, author, info, category_id, book_update_time, crawl_url, status):
        session = db_session()
        if avatar:
            md5_res = hashlib.new('md5', '%s%s%s' % (title.encode('utf-8'), author, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            avatar_file_name = 'cover/%s' % md5_res.hexdigest()
        else:
            avatar_file_name = ''

        book = Book(title=title, avatar=avatar_file_name, author=author, info=info, category_id=category_id,
                    book_update_time=book_update_time, crawl_url=crawl_url)
        session.add(book)
        try:
            session.commit()
        except:
            session.rollback()

        if avatar:
            bucket.fetch(avatar, bucket_name, key=avatar_file_name)

        return book

    @classmethod
    def update(cls, title, avatar, author, info, category_id, book_update_time, crawl_url, status):
        session = db_session()
        query = session.query(Book)
        query.filter(Book.title == title, Book.author == author).update({
            Book.info: info,
            Book.category_id: category_id,
            Book.book_update_time: book_update_time,
            Book.status: status,
        })
        try:
            session.commit()
        except:
            session.rollback()

        book = session.query(Book).filter(Book.title == title,
                                             Book.author == author).scalar()

        return book


class Chapter(BaseModel):

    __tablename__ = 'chapter'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50))
    book_id = Column(Integer)
    category_id = Column(Integer)
    chapter_path = Column(String(255))
    serial_num = Column(Integer)
    crawl_url = Column(String(255))
    create_time = Column(DateTime, default=func.now())
    update_time = Column(DateTime, onupdate=datetime.now())

    @classmethod
    def get_by_serial_num_and_book(cls, serial_num, book_id):
        session = db_session()
        chapter = session.query(Chapter).filter(Chapter.serial_num == serial_num,
                                             Chapter.book_id == book_id).scalar()
        session.close()
        return chapter


    @classmethod
    def add(cls, session, title, book_id, category_id, serial_num, chapter_path, crawl_url):
        chapter = Chapter(title=title, book_id=book_id, category_id=category_id, chapter_path=chapter_path, serial_num=serial_num,
                      crawl_url=crawl_url)
        session.add(chapter)
        session.commit()

        return chapter

    @classmethod
    def get_newest_chapter_by_book(cls, book_id):
        session = db_session()
        query = session.query(Chapter).filter(Chapter.book_id == book_id)
        chapter = query.order_by('-serial_num').first()
        return chapter

#
# class Content(BaseModel):
#
#     __tablename__ = 'content'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     content = Column(Text)
#     create_time = Column(DateTime, default=func.now())
#     update_time = Column(DateTime, default=datetime.now())
#
#     @classmethod
#     def add(cls, content):
#         session = db_session()
#         content = Content(content=content)
#         session.add(content)
#         session.commit()
#         return content

#
# def init_db():
#     engine = create_engine(DB_CONNECT_STRING, echo=True)
#     BaseModel.metadata.create_all(engine)
#
# init_db()