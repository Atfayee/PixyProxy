The task at hand is to design a REST API for PixyProxy, a Python FastAPI image generation service leveraging Large Language Model (LLM) technology. The API will facilitate the generation and management of images based on prompts.

Each image generated will have a GUID for public identification, an integer ID for internal use, a prompt, a filename, and timestamps.

The API will be structured into four layers: database, service, core, and web.

1. Database Layer: Located in the /data directory, this layer will utilize a repository pattern and MySQL database. It will implement conversions between image models and dictionaries for efficiency and utilize named parameters for SQL commands. The initialization logic will reside in an init.py module.

2. Service Layer: Located in the /service directory, this layer will handle requests for generating images from prompts and retrieving image details. It will validate incoming models from the web layer using pydantic. All exceptions, whether from the database or service layer, will be formatted as an ImageGenerationException.

3. Core Layer: Located in the /core directory, this layer will focus on image models and exceptions, all of which will extend ImageGenerationException.

4. Web Layer: Located in the /web directory, this layer will contain resources for managing images through API endpoints. It will incorporate universal request logging and exception handling.

The API will support the following endpoints:

    POST /image: Generate an image (and image detail) from a prompt. Return an ImageDetail model object that includes the prompt, filename, and GUID.

    GET /image/guid: Retrieve image details for an image with the provided GUID. Return an ImageDetail model object that includes the prompt, filename, and GUID.

    GET /image: Get image details for all images. Return a list of ImageDetail model objects that includes the prompt, filename, and GUID.

    GET /image/guid/content: Retrieve the image file using the provided GUID. Return the image bytes in the body of the HTTP response.

The API endpoints will handle both the generation and retrieval of images without requiring separate public and private sections.
