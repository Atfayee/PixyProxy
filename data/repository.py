import core
from core.models import ImageDetail, ImageDetailCreate
from core.exceptions import PromptException 
from typing import List
from data import DatabaseContext, get_current_db_context


class ImageRepositoryInterface:

    # def __init__(self):
    #     self.conn = create_connection()
    #     if not self.conn:
    #         raise DBConnectionError()

    def create_image(self, image: ImageDetailCreate) -> ImageDetail:
        # Implement the logic to create an image in the database
        pass

    def get_image(self, guid: str) -> ImageDetail:
        # Implement the logic to get an image from the database
        pass

    def get_all_images(self) -> List[ImageDetail]:
        # Implement the logic to get all images from the database
        pass

    def get_image_content(self, guid: str) -> bytes:
        # Implement the logic to get an image content from the database
        pass

class ImageRepository(ImageRepositoryInterface):
    # def __init__(self):
    #     self.conn = create_connection()
    #     if not self.conn:
    #         raise DBConnectionError()

    def create_image(self, image_create: ImageDetailCreate) -> ImageDetail:
    # def create_image(self, prompt: str) -> ImageDetail:
            # Implement the logic to create an image in the database
        db = get_current_db_context()
        with DatabaseContext() as db:
            guid = core.make_guid()
            filename = {core.make_guid()}.png

            db.cursor.execute(
                "INSERT INTO images (guid, filename, prompt) VALUES (%s, %s, %s)",
                (guid, filename, image_create.prompt)
            )
            return ImageDetail(guid=guid, filename=filename, prompt=image_create.prompt)
# 

    def get_image(self, guid: str) -> ImageDetail:
        # Use the global function to fetch the current database context
        db = get_current_db_context()
        with DatabaseContext() as db:  # This line creates a new database context
            db.cursor.execute("SELECT guid, filename, prompt FROM images WHERE guid = %s", (guid,))
            result = db.cursor.fetchone()
            if not result:
                return None  # Return None if no result is found

            # Create and return an ImageDetail instance with data from the result
            return ImageDetail(guid=result['guid'], filename=result['filename'], prompt=result['prompt'])

    def get_all_images(self) -> List[ImageDetail]:
        # Implement the logic to get all images from the database
        db = get_current_db_context()
        with DatabaseContext() as db:
            db.cursor.execute("SELECT guid, filename, prompt FROM images")
            result = db.cursor.fetchall()
            # return [ImageDetail(guid=row[0], filename=row[1], prompt=row[2]) for row in result]
            return [ImageDetail(guid=row['guid'], filename=row['filename'], prompt=row['prompt']) for row in result]


    def get_image_content(self, guid: str) -> bytes:
        # Implement the logic to get an image content from the database
        pass