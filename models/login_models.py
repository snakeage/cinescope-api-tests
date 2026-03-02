from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr

from constants.roles import Roles
from models.common import to_camel_case


class LoginUser(BaseModel):
    id: UUID
    email: EmailStr
    full_name: str
    roles: list[Roles]

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel_case
    )


class LoginResponse(BaseModel):
    user: LoginUser
    access_token: str
    refresh_token: UUID
    expires_in: int  # у тебя сейчас epoch в ms

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel_case
    )
