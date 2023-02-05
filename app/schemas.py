from typing import Optional

from pydantic import BaseModel


class NewsCreate(BaseModel):
    url: str
    title: str
    news: str


class News(BaseModel):
    id: int
    url: str
    title: Optional[str]
    news: Optional[str]

    class Config:
        orm_mode = True
