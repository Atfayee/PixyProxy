from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from core.models import User
from data.image_repository import MySQLImageRepository, ImageRepositoryInterface
from service.image_gen_service import ImageGenerationServiceInterface, ImageGenerationService

security = HTTPBasic()


def get_image_repository() -> ImageRepositoryInterface:
    return MySQLImageRepository()


def get_image_service(repo: ImageRepositoryInterface = Depends(get_image_repository)) -> ImageGenerationServiceInterface:
    return ImageGenerationService(repo)


# def require_admin_user(credentials: HTTPBasicCredentials = Depends(security),
#                        user_service: UserService = Depends(get_user_service)) -> Optional[User]:
#     user = user_service.authenticate_user(credentials.username)
#     if user is not None and credentials.password == user.password and user.username == "steve72":
#         return user
#     return None


# def require_current_user(credentials: HTTPBasicCredentials = Depends(security),
#                          user_service: UserService = Depends(get_user_service)) -> User:
#     user = user_service.authenticate_user(credentials.username)

#     if user is None or not credentials.password==user.password:
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     return user
