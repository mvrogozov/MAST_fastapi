from sqlalchemy import MetaData, Integer, Column
from sqlalchemy import String, Text
from database import Base

metadata = MetaData()


class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    title = Column(String, nullable=True)
    news = Column(Text, nullable=True)
