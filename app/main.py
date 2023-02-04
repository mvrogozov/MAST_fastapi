from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException, Request
from utils.wp_checker import NewsCollector
from database import SessionLocal, db
from sqlalchemy.orm import Session
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
) -> None:
    """Собирает новости с сайтов в базу."""

    collector.get_urls()
    for url in collector.urls:
        print(url)
        data = collector.get_news(url, per_page)
        if data == []:
            continue
        for post in data:
            if db.query(exists().where(
                models.News.title == post['title'],
                models.News.url == post['url']
            )
            ).scalar():
                continue
            news = models.News(
                title=post['title'],
                news=post['post'],
                url=post['url']
            )
            try:
                db.add(news)
                db.commit()
            except Exception as e:
                print('Ошибка записи в БД: ', e)
    db.close()
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
    ).all()
    if not news:
        raise HTTPException(
            status_code=404,
            detail=f"News with '{q}' not found"
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
