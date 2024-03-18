from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials


from data.image_repository import MySQLImageRepository, ImageRepositoryInterface
from service.image_gen_service import ImageGenerationServiceInterface, ImageGenerationService

security = HTTPBasic()


def get_image_repository() -> ImageRepositoryInterface:
    return MySQLImageRepository()


def get_image_service(repo: ImageRepositoryInterface = Depends(get_image_repository)) -> ImageGenerationServiceInterface:
    return ImageGenerationService(repo)

