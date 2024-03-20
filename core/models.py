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



# class ImageDetailCreate(BaseModel):
#     prompt: str

# class ImageDetail(ImageDetailCreate):
#     guid: Optional[str] = None
#     filename: Optional[str] = None


