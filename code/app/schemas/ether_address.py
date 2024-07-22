from typing import Optional
from pydantic import BaseModel, Field


class EtherAddressResponse(BaseModel):
    id: str = Field(..., description="id")
    user_id: str = Field(..., description="user id")
    address: str = Field(..., description="ether address")
    low_case_address: str = Field(..., description="ether address")
    created_at: str = Field(..., description="created At")

    @classmethod
    def from_ether_model(cls, ether):
        return cls(
            id=str(ether.id),
            user_id=str(ether.user_id),
            address=ether.address,
            low_case_address=ether.low_case_address,
            created_at=ether.created_at.isoformat(),
        )
