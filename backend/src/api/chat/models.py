from typing import Optional
from datetime import datetime, timezone

from sqlmodel import SQLModel, Field, DateTime

def get_utc_now():
    return datetime.now(tz=timezone.utc)

class ChatMessagePayload(SQLModel):
    # pydantic model
    # for validations 
    # serializer (meaning we could use it to validate responses from the backend/api)
    message: str

class ChatMessage(SQLModel, table=True):
    # database table
    # saving, updating, deleting, getting 
    # serializer
    id: Optional[int] = Field(default=None, primary_key=True)
    message: str
    created_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=DateTime(timezone=True), # for sqlalchemy
        primary_key=False,
        nullable=False
    )

class ChatMessageListItem(SQLModel):
    id: int = Field(default=None)
    message: str
    created_at: datetime = Field(default=None)