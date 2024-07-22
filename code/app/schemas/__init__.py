from typing import Optional

from pydantic import BaseModel, Field


class NoContentResponse(BaseModel):
    code: int = Field(204, description="Status Code")
    message: str = Field("Resource not found!", description="Exception Information")


class OKResponse(BaseModel):
    code: int = Field(0, description="Status Code")
    message: str = Field("ok", description="Exception Information")
    data: Optional[dict] = Field(None, description="Data")
