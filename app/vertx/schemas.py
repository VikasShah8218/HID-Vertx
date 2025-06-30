from pydantic import BaseModel, Field
from typing import Optional

class AddCardSchema(BaseModel):
    card_number: str = Field(..., alias="CN", min_length=1, max_length=32, description="Card number (1-32 hex digits)")
    unique_id: str = Field(..., alias="UID", min_length=1, description="Unique identifier for the credential")
    # addr: Optional[str] = Field(None, description="Controller IP address")
    # pin: Optional[str] = Field("0", max_length=15, description="User PIN (1-15 digits), 0 for card only")
    # access_type: Optional[int] = Field(1, ge=1, le=3, description="1=Card+PIN, 2=Card/PIN, 3=PIN only")