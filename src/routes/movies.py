import math
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from src.database import get_db, MovieModel
from src.schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema

router = APIRouter()


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def detail_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(MovieModel).filter(MovieModel.id == movie_id)
    result = await db.execute(stmt)
    film = result.scalars().first()

    if not film:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")

    return film


@router.get("/movies/", response_model=MovieListResponseSchema)
async def list_movies(
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=20),
        db: AsyncSession = Depends(get_db)
):
    offset = (page - 1) * per_page

    stmt_count = select(func.count()).select_from(MovieModel)
    result_count = await db.execute(stmt_count)
    total_items = result_count.scalar()

    total_pages = math.ceil(total_items / per_page)

    stmt_movies = select(MovieModel).offset(offset).limit(per_page)
    result_movies = await db.execute(stmt_movies)
    movies = result_movies.scalars().all()

    return {
        "movies": movies,
        "total": total_items,
        "total_pages": total_pages,
        "per_page": per_page,
        "current_page": page,
        "next_page": page + 1 if page < total_pages else None,
        "prev_page": page - 1 if page > 1 else None
    }
