# Define database repository interface
# Include methods for CRUD operations on the images table
# Use DB-API to interact with MySQL backend
import base64
import os
from typing import List, Literal, Optional
from urllib.parse import urlparse
from fastapi import Response
from openai import OpenAI
import requests
import core
from core.models import ImageDetail, ImageDetailCreate
from data import get_current_db_context

class ImageRepositoryInterface:

    def created_image(self, prompt:ImageDetailCreate)->ImageDetail:
        # Implementation of the generate-image use case
        pass

    def get_all_images(self)->List[ImageDetail]:
        # Implementation of the list-all-images use case
        pass

    def get_image_by_guid(self, guid:str)->ImageDetail:
        # Implementation of the get-image use case
        pass

    def get_image_content(self, guid:str)->bytes:
        # Implementation of the get-image-content use case
        pass


class ImageGenerator:
    def __init__(self, repository: ImageRepositoryInterface, base_url='http://aitools.cs.vt.edu:7860/openai/v1',
                 api_key='aitools', ):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.repo = repository
    
    def generate_image(self, image_create_request: ImageDetailCreate, model: str = "dall-e-3",
                   style: Literal["vivid", "natural"] = "vivid",
                   quality: Literal["standard", "hd"] = "hd",
                   size: Literal["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"] = "1024x1024") -> ImageDetail:
            # call open AI
            # get the image url from the OpenAI response
            response = self.client.images.generate(
                model=model,
                prompt="a rubber duck on a sink",
                style=style,
                quality=quality,
                size=size,
                timeout=100
            )
            # using httpx or requests, get the contents of the image url
            # save the contents of the image underneath the images folder
            # print(response.data[0])
            image_url = response.data[0].url
            print(image_url)
            response = requests.get(image_url)
            filename = os.path.basename(urlparse(image_url).path)
            # print("Saving image to", filename)
            # Open a file in write mode and save the image to it
            with open(filename, 'wb') as file:
                file.write(response.content)
            # make a guid for the image
            guid = core.make_guid()
            # using self.repo, save the guid, filename and prompt to the database
            return ImageDetail(guid=guid, filename=filename,prompt=image_create_request.prompt)



class MySQLImageRepository(ImageRepositoryInterface):

    def created_image(self, image: ImageDetailCreate):
        db = get_current_db_context()
        
        image_guid = core.make_guid()
        # Generate filename based on the prompt
        # Create an instance of ImageGenerator
        image_generator = ImageGenerator(repository=self)
        image_detail = image_generator.generate_image(image_create_request=image)
        db.cursor.execute(
            "INSERT INTO images (guid, filename, prompt) VALUES (%s, %s, %s)",
            (image_detail.guid, image_detail.filename, image.prompt)
        )

        return image_detail
    

    def get_image_by_guid(self, guid: str) -> ImageDetail:
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

        return ImageDetail(**self.make_result_dict(result))


    def get_image_content(self, guid: str) -> bytes:
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

        image_detail = ImageDetail(**self.make_result_dict(result))

        with open(image_detail.filename,"rb") as file:
            return file.read()



    def get_all_images(self) -> List[ImageDetail]:
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
            "guid": result["guid"],
            "filename": result["filename"],
            "prompt": result["prompt"],
            "created_at": result["created_at"],
            "updated_at": result["updated_at"],
        }
        return result_dict