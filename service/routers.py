
from fastapi import APIRouter, HTTPException
from core.models import ImageCreateResponse, GetImageDetailResponse, GetAllImagesResponse
from service.image_generation_service_interface import ImageGenerationServiceInterface
from core.exceptions import ImageGenerationException

image_router = APIRouter()

@image_router.post("/image", response_model=ImageCreateResponse)
async def generate_image(prompt: str, service: ImageGenerationServiceInterface):
    try:
        image_detail = service.generate_image(prompt)
        return {"detail": image_detail}
    except ImageGenerationException as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@image_router.get("/image/{guid}", response_model=GetImageDetailResponse)
async def get_image_details(guid: str, service: ImageGenerationServiceInterface):
    try:
        image_detail = service.retrieve_image_details(guid)
        return {"detail": image_detail}
    except ImageGenerationException as exc:
        raise HTTPException(status_code=404, detail=str(exc))

@image_router.get("/image", response_model=GetAllImagesResponse)
async def get_all_images(service: ImageGenerationServiceInterface):
    try:
        image_details = service.list_all_images()
        return {"images": image_details}
    except ImageGenerationException as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@image_router.get("/image/{guid}/content")
async def get_image_content(guid: str, service: ImageGenerationServiceInterface):
    try:
        image_content = service.retrieve_image_content(guid)
        return image_content
    except ImageGenerationException as exc:
        raise HTTPException(status_code=404, detail=str(exc))