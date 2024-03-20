Here are the system use cases for the image generating system:

1. **Create a Image**: This use case involves generating a new image from a prompt. The user must provide a description. For example, my prompt is generate a yellow duck for me. The system will generate a GUID, filename and content detail for the actual image and store them in the database. 
The system will return the ImageDetail model object(see below) that includes prompt, filename and guid.

2. **Get a image**: This use case involves getting image details for an image with the provided {guid}. 
The system will return the ImageDetail model object(see below) that includes prompt, filename and guid.

3. **Get all images**: This use case involves getting all image details for all images from the database.
The system will return a list of ImageDetail object(see below).

4. **Get an image content**: This use case involves retrieving image file using the provided GUID, and return to the user.
The system will return the image bytes in the body of the HTTP response.


from pydantic import BaseModel

class ImageDetailCreate(BaseModel):
    prompt: str

class ImageDetail(ImageDetailCreate):
    guid: str
    filename: str