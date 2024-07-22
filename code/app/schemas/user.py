from typing import Optional
from pydantic import BaseModel, Field


class UserBody(BaseModel):
    mail: str = Field(None, description="mail")
    password: Optional[str] = Field(None, description="password")


class UserPath(BaseModel):
    id: str = Field(..., description="id")


class UserResponse(BaseModel):
    id: str = Field(..., description="id")
    mail: str = Field(..., description="mail")
    created_at: str = Field(..., description="created At")

    @classmethod
    def from_user_model(cls, user):
        return cls(
            id=str(user.id),
            mail=user.mail,
            created_at=user.created_at.isoformat(),
        )
