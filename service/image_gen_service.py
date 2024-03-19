# service/prompt_service.py
import traceback
from typing import List, Optional

from pydantic import ValidationError

from core.exceptions import ImageGenerationException, ConstraintViolationError, DataValidationError
from core.models import ImageDetail, ImageDetailCreate
from data import DatabaseContext
from data.image_repository import ImageRepositoryInterface


class ImageGenerationServiceInterface:
    def generate_image(self, prompt: ImageDetailCreate) -> ImageDetail:
        """
        Generate a new image in the database.

        Args:
            prompt (ImageDetailCreate): The prompt to generate image.

        Returns:
            ImageDetail: The image detail obj of the generated image.

        Raises:
            ConstraintViolationError: If the prompt data is invalid.
            ImageGenerationException: If an unexpected error occurs.
            :param prompt:
        """
        pass

    

    def get_image(self, guid: str) -> ImageDetail:
        """
        Retrieves an image by its GUID.

        Args:
            guid (str): The GUID of the image to retrieve.

        Returns:
            Prompt: The retrieved image model.

        Raises:
            ImageGenerationException: If an unexpected error occurs.
            :param guid:
        """
        pass
    

    def list_images(self) -> List[ImageDetail]:
        """
        Retrieves all images.

        Returns:
            List[ImageDetail]: A list of all image obj.

        Raises:
            ImageGenerationException: If an unexpected error occurs.
        """
        pass


    def get_iamge_content(self, guid:str)->bytes:
        """
        Retrieves an image content by its GUID.

        Returns:
            bytes: The image bytes in the body of the HTTP response.

        Raises:
            ImageGenerationException: If an unexpected error occurs.
        """
        pass    

    

class ImageGenerationService(ImageGenerationServiceInterface):
    def __init__(self, image_repository: ImageGenerationServiceInterface):
        self.image_repository = image_repository

    def generate_image(self, prompt: ImageDetailCreate) -> ImageDetail:
        try:
            prompt = ImageDetailCreate(**prompt.dict())
        except ValidationError as e:
            raise ConstraintViolationError(str(e))

        with DatabaseContext() as db:
            try:
                db.begin_transaction()
                # guid = self.image_repository.generate_image(prompt)
                image = self.image_repository.generate_image(prompt)
                db.commit_transaction()
                return image.guid
            except ImageGenerationException as known_exc:
                traceback.print_exc()
                db.rollback_transaction()
                raise known_exc
            except Exception as e:
                traceback.print_exc()
                db.rollback_transaction()
                raise ImageGenerationException("An unexpected error occurred while processing your request.") from e

    
    def get_image(self, guid:str)->ImageDetail:
        with DatabaseContext():
            try:
                return self.image_repository.get_image(guid)
            except ImageGenerationException as known_exc:
                traceback.print_exc()
                raise known_exc
            except Exception as e:
                traceback.print_exc()
                raise ImageGenerationException("An unexpected error occurred while processing your request.") from e

    
    def list_images(self)->List[ImageDetail]:
        with DatabaseContext():
            try:
                return self.image_repository.list_images()
            except ImageGenerationException as known_exc:
                traceback.print_exc()
                raise known_exc
            except Exception as e:
                traceback.print_exc()
                raise ImageGenerationException("An unexpected error occurred while processing your request.") from e

    