from fastapi import FastAPI, BackgroundTasks
from time import sleep
from utils.wp_checker import NewsCollector, collect_news
from database import db, News

app = FastAPI()

collector = NewsCollector()

@app.get('/news')
def get_news():
    news = News(
        title='TestFast',
        url='fasturl',
        news='fastfastfastfastfastfastfast'
    )
    db.add(news)
    db.commit()
    return 'get newss'


def sleeping_func():
    collect_news(collector, 10)
    collector.in_progress = False


@app.get('/collect')
async def go_to_bed(background_tasks: BackgroundTasks):
    if collector.in_progress:
        return {"message": "collecting still in progress"}
    collector.in_progress = True
    background_tasks.add_task(sleeping_func)
    return {"message": "collecting started"}
