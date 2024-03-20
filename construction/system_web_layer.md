To build the web layer for the PixyProxy system, we will follow these steps:

Import the necessary modules and classes.
Create a FastAPI application instance.
Define the API models.
Define the API routes.
Implement the API endpoints.
Implement the global dependency for logging.
Implement the exception handler.
Here is the Python code for the web layer:

from fastapi import FastAPI, Depends, HTTPException
from typing import List
from pydantic import BaseModel
from datetime import datetime
import logging
from uuid import uuid4

# Import the service layer
from service import ImageDetailService

# Import the core models and exceptions
from core import ImageDetailCreate, ImageDetail, PromptException, EXCEPTION_STATUS_CODES

app = FastAPI()

# Initialize the service layer
service = ImageDetailService()

class ImageDetailCreateRequest(BaseModel):
    prompt: str

class ImageDetailResponse(BaseModel):
    guid: str
    filename: str
    prompt: str

@app.post("/image", response_model=ImageDetailResponse)
def create_image(image: ImageDetailCreateRequest):
    image_detail = service.create_image(ImageDetailCreate(prompt=image.prompt))
    return ImageDetailResponse(guid=image_detail.guid, filename=image_detail.filename, prompt=image_detail.prompt)

@app.get("/image/{guid}", response_model=ImageDetailResponse)
def get_image(guid: str):
    image_detail = service.get_image(guid)
    return ImageDetailResponse(guid=image_detail.guid, filename=image_detail.filename, prompt=image_detail.prompt)

@app.get("/image", response_model=List[ImageDetailResponse])
def get_all_images():
    images = service.get_all_images()
    return [ImageDetailResponse(guid=image.guid, filename=image.filename, prompt=image.prompt) for image in images]

@app.get("/image/{guid}/content")
def get_image_content(guid: str):
    return service.get_image_content(guid)

@app.middleware("http")
async def log_requests(request, call_next):
    request_id = str(uuid4())
    logging.info(f"{datetime.now()} INFO {request_id} REQUEST START {request.method} {request.url.path}")
    response = await call_next(request)
    logging.info(f"{datetime.now()} INFO {request_id} REQUEST END {request.method} {request.url.path}")
    return response

@app.exception_handler(PromptException)
async def handle_prompt_exception(request, exc):
    return HTTPException(status_code=EXCEPTION_STATUS_CODES[type(exc)], detail=str(exc))

    This code creates a FastAPI application with four endpoints: /image (POST), /image/{guid} (GET), /image (GET), and /image/{guid}/content (GET). It also includes a middleware for logging all requests and an exception handler for handling all exceptions derived from PromptException.