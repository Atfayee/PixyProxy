from fastapi import FastAPI, Depends, HTTPException, APIRouter
from typing import List
from pydantic import BaseModel
from datetime import datetime
import logging
from uuid import uuid4

# Import the service layer
from service.image_service import ImageDetailService

# Import the core models and exceptions
from core.models import ImageDetailCreate, ImageDetail
from core.exceptions import PromptException, EXCEPTION_STATUS_CODES

# app = FastAPI()
router = APIRouter()


# Initialize the service layer
service = ImageDetailService()

class ImageDetailCreateRequest(BaseModel):
    prompt: str

class ImageDetailResponse(BaseModel):
    guid: str
    filename: str
    prompt: str



@router.post("/", response_model=ImageDetailResponse, summary="Generate a new image")
async def create_image(prompt: str):
    image_detail = service.create_image(ImageDetailCreate(prompt=prompt))
    # image_detail = service.create_image(prompt)
    # print("image_detail", image_detail)
    return ImageDetailResponse(guid=image_detail.guid, filename=image_detail.filename, prompt=image_detail.prompt)

@router.get("/{guid}", response_model=ImageDetailResponse, summary="Get image details by GUID")
async def get_image(guid: str):
    image_detail = service.get_image(guid)
    return ImageDetailResponse(guid=image_detail.guid, filename=image_detail.filename, prompt=image_detail.prompt)

@router.get("/", response_model=List[ImageDetailResponse], summary="Get details of all images")
async def get_all_images():
    images = service.get_all_images()
    return [ImageDetailResponse(guid=image.guid, filename=image.filename, prompt=image.prompt) for image in images]

@router.get("/{guid}/content", summary="Get image content by GUID")
async def get_image_content(guid: str):
    return service.get_image_content(guid)



# @router.post("/", response_model=ImageDetailResponse, summary="Generate a new image")
# def create_image(prompt: str):
#     image_detail = service.create_image(ImageDetailCreate(prompt=prompt))
#     # image_detail = service.create_image(prompt)
#     print("image_detail", image_detail)
#     return ImageDetailResponse(guid=image_detail.guid, filename=image_detail.filename, prompt=image_detail.prompt)

# @router.get("/{guid}", response_model=ImageDetailResponse, summary="Get image details by GUID")
# def get_image(guid: str):
#     image_detail = service.get_image(guid)
#     return ImageDetailResponse(guid=image_detail.guid, filename=image_detail.filename, prompt=image_detail.prompt)

# @router.get("/", response_model=List[ImageDetailResponse], summary="Get details of all images")
# def get_all_images():
#     images = service.get_all_images()
#     return [ImageDetailResponse(guid=image.guid, filename=image.filename, prompt=image.prompt) for image in images]

# @router.get("/{guid}/content", summary="Get image content by GUID")
# def get_image_content(guid: str):
#     return service.get_image_content(guid)

# @router.middleware("http")
# async def log_requests(request, call_next):
#     request_id = str(uuid4())
#     logging.info(f"{datetime.now()} INFO {request_id} REQUEST START {request.method} {request.url.path}")
#     response = await call_next(request)
#     logging.info(f"{datetime.now()} INFO {request_id} REQUEST END {request.method} {request.url.path}")
#     return response

# @router.exception_handler(PromptException)
# async def handle_prompt_exception(request, exc):
#     return HTTPException(status_code=EXCEPTION_STATUS_CODES[type(exc)], detail=str(exc))