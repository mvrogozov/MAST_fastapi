from sqlalchemy import MetaData, Integer, Table, Column, TIMESTAMP, JSON
from sqlalchemy import String, ForeignKey, Boolean, Text
from database import Base

metadata = MetaData()

# news = Table(
#     'news',
#     metadata,
#     Column('id', Integer, primary_key=True),
#     Column('url', String),
#     Column('title', String, nullable=True),
#     Column('news', Text)
# )


class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    title = Column(String, nullable=True)
    news = Column(Text, nullable=True)
