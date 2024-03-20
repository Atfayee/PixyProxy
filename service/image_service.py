# service/image_service.py
from pydantic import ValidationError
from core.models import ImageDetailCreate, ImageDetail
from core.exceptions import PromptException, RecordNotFoundError
from data.repository import ImageRepository
from typing import List

class ImageDetailServiceInterface:
    def create_image(self, prompt: str) -> ImageDetail:
        raise NotImplementedError

    def get_image(self, guid: str) -> ImageDetail:
        raise NotImplementedError

    def get_all_images(self) -> List[ImageDetail]:
        raise NotImplementedError

    def get_image_content(self, guid: str) -> bytes:
        raise NotImplementedError

class ImageDetailService(ImageDetailServiceInterface):
    def __init__(self):
        self.repo = ImageRepository()

    def create_image(self, image_create: ImageDetailCreate) -> ImageDetail:
        try:
            return self.repo.create_image(ImageDetailCreate(prompt=image_create.prompt))
        except ValidationError as e:
            raise PromptException(e)

    def get_image(self, guid: str) -> ImageDetail:
        try:
            image = self.repo.get_image(guid)
            if not image:
                raise RecordNotFoundError(f"No image found with guid {guid}")
            return image
        except ValidationError as e:
            raise PromptException(e)

    def get_all_images(self) -> List[ImageDetail]:
        try:
            return self.repo.get_all_images()
        except ValidationError as e:
            raise PromptException(e)

    def get_image_content(self, guid: str) -> bytes:
        try:
            return self.repo.get_image_content(guid)
        except ValidationError as e:
            raise PromptException(e)