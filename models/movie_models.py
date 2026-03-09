from datetime import datetime

from pydantic import BaseModel, ConfigDict, StrictBool

from models.common import to_camel_case


class MovieResponse(BaseModel):
    id: int
    name: str
    price: int | float
    location: str
    genre_id: int
    published: StrictBool
    created_at: datetime

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel_case)


class MoviesListResponse(BaseModel):
    movies: list[MovieResponse]
    page: int
    page_size: int

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel_case)
