# core/models.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ImageDetailCreate(BaseModel):
    prompt: str

class ImageDetailUpdate(ImageDetailCreate):
    guid: Optional[str] = None
    filename: Optional[str] = None

class ImageDetail(ImageDetailUpdate):
    id: int
    created_at: datetime
    updated_at: datetime



# core/exceptions.py
class PromptException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class DBConnectionError(PromptException):
    def __init__(self):
        super().__init__("A connection to the database could not be established")

class RecordNotFoundError(PromptException):
    def __init__(self):
        super().__init__("The requested record was not found")

class ConstraintViolationError(PromptException):
    def __init__(self):
        super().__init__("A database constraint was violated")
        