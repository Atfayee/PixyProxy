from fastapi import APIRouter, Depends, HTTPException
from core.exceptions import RecordNotFoundError
from core.models import ImageDetail, ImageDetailCreate
from service.image_gen_service import ImageGenerationServiceInterface
from typing import List
from web.dependencies import get_image_service

router = APIRouter()


@router.post("/image/", status_code=201, summary="Generate a new image.")
async def generate_image(prompt: ImageDetailCreate,
                         service: ImageGenerationServiceInterface = Depends(get_image_service)):
    return service.generate_image(prompt)


@router.get("/image/{guid}", response_model=ImageDetail, summary="Retrieve an image by GUID.")
def get_image(guid: str, service: ImageGenerationServiceInterface = Depends(get_image_service)):
    try:
        return service.get_image(guid)
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Image not found")


@router.get("/image/", response_model=List[ImageDetail], summary="List all images.")
def list_images(skip: int = 0, limit: int = 10, service: ImageGenerationServiceInterface = Depends(get_image_service)):
    return service.list_images()[skip: skip + limit]


@router.get("/image/{guid}/content", response_model=bytes, summary="Retrieve an Image content by GUID.")
def get_image_content(guid: str, service: ImageGenerationServiceInterface = Depends(get_image_service)):
    try:
        return service.get_image_content(guid)
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Image not found")

