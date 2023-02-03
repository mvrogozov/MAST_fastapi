from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException, status, Request
from time import sleep
from utils.wp_checker import NewsCollector
from database import SessionLocal, db
from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.sql import exists
from typing import List
import models
import schemas


app = FastAPI()

collector = NewsCollector()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def collect_news(
    collector: NewsCollector,
    per_page: int,
    session: Session = get_session()
) -> None:
    """Собирает новости с сайтов в базу."""

    collector.get_urls()
    for url in collector.urls:
        print(url)
        data = collector.get_news(url, per_page)
        if data == []:
            continue
        for post in data:
            #session.query(User.query.filter(User.id == 1).exists()).scalar()
            #session.query(exists().where(User.email == '...')).scalar()
            #if db.query(models.News).filter(and_(models.News.title == post['title'], models.News.url == post['url'])).exists().scalar():
            if db.query(exists().where(models.News.title == post['title'], models.News.url == post['url'])).scalar():
                print('exists')
                continue
            news = models.News(
                title=post['title'],
                news=post['post'],
                url=post['url']
            )
            db.add(news)
            db.commit()
    print('Collecting finished')


@app.get("/news/", response_model=List[schemas.News])
def read_news(request: Request, session: Session = Depends(get_session)):
    q = str(request.query_params)
    mystr = q[2:]
    try:
        encoded_str = bytes.fromhex(mystr.replace('%', ''))
        string = encoded_str.decode('utf-8')
    except ValueError:
        string = mystr

    news = session.query(models.News).filter(
        models.News.title.contains(string) | models.News.news.contains(string)
    ).all()[:10]
    if not news:
        raise HTTPException(
            status_code=404,
            detail=f"todo item with id {q} not found"
        )
    return news


def collect():
    collect_news(collector, 10)
    collector.in_progress = False


@app.get('/collect')
async def start_collecting(background_tasks: BackgroundTasks):
    if collector.in_progress:
        return {"message": "collecting still in progress"}
    collector.in_progress = True
    background_tasks.add_task(collect)
    return {"message": "collecting started"}
