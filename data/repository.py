# Define database repository interface
# Include methods for CRUD operations on the images table
# Use DB-API to interact with MySQL backend
from typing import List, Optional
from fastapi import Response
import core
from core.models import ImageDetail, ImageDetailCreate
from data import get_current_db_context

class ImageRepositoryInterface:

    def generate_image(self, prompt:ImageDetailCreate)->ImageDetail:
        # Implementation of the generate-image use case
        pass

    def list_images(self)->List[ImageDetail]:
        # Implementation of the list-all-images use case
        pass

    def get_image(self, guid:str)->ImageDetail:
        # Implementation of the get-image use case
        pass

    def get_iamge_content(self, guid:str)->bytes:
        # Implementation of the get-image-content use case
        pass

class MySQLImageRepository(ImageRepositoryInterface):

    def generate_image(self, image: ImageDetailCreate):
        db = get_current_db_context()
        image_guid = core.make_guid()
        db.cursor.execute(
            "INSERT INTO images (guid, filename, prompt) VALUES (%s, %s, %s)",
            (image_guid, image.filename, image.prompt)
        )
        result_dict = self.make_result_dict(image)
        return ImageDetail(**result_dict)
    

    def get_image(self, guid: str) -> ImageDetail:
        db = get_current_db_context()
        # Base SQL query
        sql = """
            SELECT * FROM images WHERE guid = %s
        """
        # Parameters for SQL query
        params = [guid]
        db.cursor.execute(sql, params)
        result = db.cursor.fetchone()

        if result is None:
            raise core.exceptions.RecordNotFoundError("Image not found")

        # Access the result via column names
        result_dict = self.make_result_dict(result)

        return ImageDetail(**result_dict)

    def get_iamge_content(self, guid: str) -> str:
        db = get_current_db_context()
        # Base SQL query
        sql = """
            SELECT * FROM images WHERE guid = %s
        """
        # Parameters for SQL query
        params = [guid]
        db.cursor.execute(sql, params)
        result = db.cursor.fetchone()

        if result is None:
            raise core.exceptions.RecordNotFoundError("Image not found")

        # Create a response with image data
        response = Response(content=result)
        response.headers["Content-Type"] = "image/jpeg"  # Adjust content type based on your image format
        return response


    def list_images(self) -> List[ImageDetail]:
        db = get_current_db_context()

        # Base SQL query
        sql = """
            SELECT * FROM images
        """

        # Parameters for SQL query
        params = []

        db.cursor.execute(sql, params)
        results = db.cursor.fetchall()
        return [ImageDetail(**self.make_result_dict(result)) for result in results]
    




    @staticmethod
    def make_result_dict(result):
        result_dict = {
            "id": result["id"],
            "file_name": result["file_name"],
            "prompt": result["prompt"],
            "guid": result["guid"],
            "created_at": result["created_at"],
            "updated_at": result["updated_at"],
        }
        return result_dict