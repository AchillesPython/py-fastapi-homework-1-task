from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import date


class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str
    date: datetime.date
    score: float
    genre: str
    overview: str
    crew: str
    orig_title: str
    status: str
    orig_lang: str
    budget: float
    revenue: float
    country: str

    model_config = ConfigDict(from_attributes=True)


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    total: int
    total_pages: int
    per_page: int
    current_page: int
    next_page: int | None
    prev_page: int | None

    model_config = ConfigDict(from_attributes=True)
