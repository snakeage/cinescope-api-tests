from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, StrictBool, ConfigDict

from constants.roles import Roles
from models.common import to_camel_case


class GetUserResponse(BaseModel):
    id: UUID
    email: EmailStr
    full_name: str
    roles: list[Roles]
    verified: StrictBool
    banned: StrictBool
    created_at: datetime

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel_case
    )
