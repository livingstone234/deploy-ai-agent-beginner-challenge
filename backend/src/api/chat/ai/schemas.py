from pydantic import BaseModel, Field


# used for validations
class EmailMessageSchema(BaseModel):
    subject: str
    contents: str
    invalid_request: bool = Field(default=False)