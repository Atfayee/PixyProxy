The task at hand is to design a REST API using Python's FastAPI framework. The API provides API endpoints for generating images from prompts, remembering the metadata and content of the generated images, listing image details, and returning image content. Each image will have a GUID for public identification, an integer ID for internal use, prompt, a filename, and timestamps.

The API will be structured into four layers: database, service, core, and web.

1. The database layer, located in the /data directory, will use a repository pattern and MySQL. It will implement conversions between models and dictionaries for efficiency and use named parameters for SQL commands. The initialization logic will be contained in an init.py module.

2. The service layer, located in the /service directory, will handle requests for public and private prompts in separate modules. It will revalidate incoming models from the web layer using pydantic. All exceptions, whether they originate from the database or service layer, will be formatted as a PromptException.

3. The core layer, located in the /core directory, will focus on models and exceptions, all of which will extend PromptException.

4. The web layer, located in the /web directory, will contain separate resources for managing public and private prompts. It will use a dependency pattern to ensure that private resource methods require authentication. It will also incorporate a dependency for universal logging of all requests.

The API will support various functionalities through its endpoints. These include searching by guid and requesting all images with pagination constraints. All responses will be in JSON format. Users will also have access for images, image details or image bytes and adding images.
