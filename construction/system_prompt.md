You are an expert Python FastAPI architect.

Design a FastAPI REST API to generate images from prompts.

Images have GUIDs, file names, prompts, and timestamps.

Structure the API using database, service, core, and web layers:

- The `/data` database layer should use a repository pattern, and use MySQL.
  Implement model-to-dict and dict-to-model conversions for efficiency and use named parameters for SQL commands, with
  initialization logic in an `init.py` module.

- The `/service` layer should revalidate the incoming
  models from the web layer and handle them with pydantic. All exceptions, originating from the database or service
  layer, should use a general `ImageGenerationException` format.

- The `/core` layer focuses on models and exceptions—all extending `ImageGenerationException`.

Endpoints will support functionality like searching by guid, requesting all images, and image bytes in the http response body. These will return JSON responses.
