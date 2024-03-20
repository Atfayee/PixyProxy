Lets build the web layer for the following system and service layer.
Let's use FastAPI to do this.

The system description is as follows:
The project at hand is the development of a Python FastAPI image generation service named PixyProxy, utilizing LLM technology. This service will later be integrated into a larger system called Ducky.

PixyProxy's primary function is to offer API endpoints that generate images from prompts. It also stores the metadata and content of these generated images. The service provides a list of image details and returns the image content. To ensure the system's functionality can be tested and graded, a specific API structure is agreed upon.

The API is divided into four main layers: database, service, core, and web.

The database layer, found in the /data directory, employs a repository pattern and uses MySQL. It is responsible for converting between models and dictionaries for efficiency and uses named parameters for SQL commands. The initialization logic is housed in an init.py module.

The service layer, located in the /service directory, manages requests. It revalidates incoming models from the web layer using pydantic. Any exceptions, whether they come from the database or service layer, are formatted as an ImageException.

The core layer, in the /core directory, concentrates on models and exceptions. All exceptions in this layer extend from ImageException.

The web layer, in the /web directory, contains separate resources for image management. It includes a dependency for universal logging of all requests.

The API offers various functionalities through its endpoints. These include generating an image (and image detail) from a prompt, retrieving details of a specific image, getting details of all images, and fetching an image file using a provided GUID. All responses from these endpoints are in JSON format.

The API also features universal request logging in a specific format: YYYY-MM-DD HH:min:sec,ms {{LoggingLevel}} {{request-id}} [thread-id] [method:line number] REQUEST START (or REQUEST END). The request-id is generated from the host-datetime-threadid. A single exception handler manages all exceptions.


Let's make sure to cover the following use cases for our system:
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
    

Here is the prompt service interface to use:
```
class ImageDetailServiceInterface:
    def create_image(self, image: ImageDetailCreate) -> ImageDetail:
        raise NotImplementedError

    def get_image(self, guid: str) -> ImageDetail:
        raise NotImplementedError

    def get_all_images(self) -> List[ImageDetail]:
        raise NotImplementedError

    def get_image_content(self, guid: str) -> bytes:
        raise NotImplementedError
```

And the ImageDetailService class:
```
class ImageDetailService(ImageDetailServiceInterface):
    def __init__(self):
        self.repo = ImageRepository()

    def create_image(self, image: ImageDetailCreate) -> ImageDetail:
        try:
            return self.repo.create_image(image)
        except ValidationError as e:
            raise ImageException(e)

    def get_image(self, guid: str) -> ImageDetail:
        try:
            image = self.repo.get_image(guid)
            if not image:
                raise RecordNotFoundError(f"No image found with guid {guid}")
            return image
        except ValidationError as e:
            raise ImageException(e)

    def get_all_images(self) -> List[ImageDetail]:
        try:
            return self.repo.get_all_images()
        except ValidationError as e:
            raise ImageException(e)

    def get_image_content(self, guid: str) -> bytes:
        try:
            return self.repo.get_image_content(guid)
        except ValidationError as e:
            raise ImageException(e)
```

Here are the core model objects to use:
```
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ImageDetailCreate(BaseModel):
    prompt: str

class ImageDetailUpdate(ImageDetailCreate):
    guid: Optional[str] = None
    filename: Optional[str] = None

class ImageDetail(ImageDetailUpdate):
    id: int
    created_at: datetime
    updated_at: datetime
```


Here are the core exceptions to use:
```
class PromptException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class DBConnectionError(PromptException):
    def __init__(self):
        super().__init__("A connection to the database could not be established")

class RecordNotFoundError(PromptException):
    def __init__(self):
        super().__init__("The requested record was not found")

class ConstraintViolationError(PromptException):
    def __init__(self):
        super().__init__("A database constraint was violated")

# 2. Service Layer Exceptions

class DataValidationError(PromptException):
    def __init__(self, message="Provided data is invalid."):
        super().__init__(message)


class OperationNotAllowedError(PromptException):
    def __init__(self, message="This operation is not allowed."):
        super().__init__(message)


# 3. Web Layer Exceptions

class BadRequestError(PromptException):
    def __init__(self, message="Bad request data."):
        super().__init__(message)


class EndpointNotFoundError(PromptException):
    def __init__(self, message="Endpoint not found."):
        super().__init__(message)


EXCEPTION_STATUS_CODES = {
    DataValidationError: 400,       # Bad Request
    ConstraintViolationError: 409,  # Conflict
    PromptException: 502,           # Internal Server Error (Generic fallback)
    DBConnectionError: 501,         # Internal Server Error (Generic fallback)
    RecordNotFoundError: 404,       # Not Found
    OperationNotAllowedError: 403,  # Forbidden
    BadRequestError: 400,           # Bad Request
    EndpointNotFoundError: 404,     # Not Found
}

```

The web layer is responsible for validation, central exception handling with a single exception handler,
and logging of each request (assigning a request id, logging the start and end result of each request per above).

Let's create a FastAPI application with 4 routers, they are:
- /image(POST)
- /image/{guid} GET
- /image GET
- /image/{guid}/content GET


Let's write a global dependency so all endpoints are logged using the required format.

Let's generate a file at a time and pause to think upfront about how things will all fit together.

Then let's generate an API description with enough detail to write test cases for the web layer.