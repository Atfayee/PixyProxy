from pydantic import BaseModel
from datetime import datetime

class ImageDetailCreate(BaseModel):
    prompt: str
    filename: str


class ImageDetail(ImageDetailCreate):
    id: int
    guid: str
    created_at: datetime
    updated_at: datetime
    filename: str