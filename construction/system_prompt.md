The goal of this project is to continue our development journey and develop another Python FastAPI image generation service, called PixyProxy, using LLM technology.  Later, we will integrate this service into Ducky.

# Mission of PixyProxy #

PixyProxy provides API endpoints for generating images from prompts, remembering the metadata and content of the generated images, listing image details, and returning image content.  Because we are going to run tests for grading, we need to agree on an API. 

The API will be structured into four layers: database, service, core, and web.

1. The database layer, located in the `/data` directory, will use a repository pattern and MySQL. It will implement
   conversions between models and dictionaries for efficiency and use named parameters for SQL commands. The
   initialization logic will be contained in an `init.py` module.

2. The service layer, located in the `/service` directory, will handle requests. It will revalidate incoming models from the web layer using pydantic. All exceptions, whether they originate from the database or service layer, will be formatted as a `ImageException`.

3. The core layer, located in the `/core` directory, will focus on models and exceptions, all of which will
   extend `ImageException`.

4. The web layer, located in the `/web` directory, will contain separate resources for managing
   images. It will incorporate a dependency for universal logging of all requests.

The API will support various functionalities through its endpoints. These include Generate an image (and image detail) from a prompt, get one image details, get all image details, and retrieve image file using the provided GUID. All responses will be in JSON format.

The API will also implement universal request logging in the
format `YYYY-MM-DD HH:min:sec,ms {{LoggingLevel}} {{request-id}} [thread-id] [method:line number] REQUEST START  (or REQUEST END)`.
The request-id will be generated from the host-datetime-threadid. All exceptions will be handled by a single exception
handler.
