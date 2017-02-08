# coding: utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_CONNECT_STRING = 'mysql+mysqldb://root:root@127.0.0.1/mybook?charset=utf8'
engine = create_engine(DB_CONNECT_STRING)
db_session = sessionmaker(bind=engine)