from pydantic import BaseModel, ConfigDict

from models.common import to_camel_case

class ErrorResponse(BaseModel):
    status_code: int
    message: str
    error: str | None = None

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel_case
    )