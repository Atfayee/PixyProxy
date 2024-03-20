from fastapi import APIRouter, Depends, HTTPException, Response
from core.exceptions import RecordNotFoundError
from core.models import ImageDetail, ImageDetailCreate
from service.image_gen_service import ImageGenerationServiceInterface
from typing import List
from web.dependencies import get_image_service

router = APIRouter()


@router.post("/image/", status_code=200, summary="Generate a new image.")
async def created_image(prompt: ImageDetailCreate,
                         service: ImageGenerationServiceInterface = Depends(get_image_service)):
    return service.created_image(prompt)


@router.get("/image/{guid}", response_model=ImageDetail, summary="Retrieve an image by GUID.")
def get_image_by_guid(guid: str, service: ImageGenerationServiceInterface = Depends(get_image_service)):
    try:
        return service.get_image_by_guid(guid)
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Image not found")


@router.get("/image/", response_model=List[ImageDetail], summary="List all images.")
def get_all_images(skip: int = 0, limit: int = 10, service: ImageGenerationServiceInterface = Depends(get_image_service)):
    return service.get_all_images()[skip: skip + limit]


@router.get("/image/{guid}/content", response_model=bytes, summary="Retrieve an Image content by GUID.")
def get_image_content(guid: str, service: ImageGenerationServiceInterface = Depends(get_image_service)):
    try:
        image_content = service.get_image_content(guid)
        response = Response(content=image_content, media_type="image/png")
        return response
    except RecordNotFoundError:
        raise HTTPException(status_code=404, detail="Image not found")

