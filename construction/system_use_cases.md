Here are the system use cases for the image generation system:

1. Generate an Image from Prompt: This use case involves generating a new image from a provided prompt. The user must provide the prompt or generating the image. The system will generate a GUID for the image and store it in the database. The system will return the `ImageDetail` object that includes prompt, filename and guid of the newly generated image.

2. List All Images: This use case involves retrieving all images details for all images. The system will return a list of `ImageDetail` model object that includes prompt, filename and guid.

3. Retrieve Image Details: This use case involves retrieving details of an existing image by its GUID. The user must provide the GUID of the image they wish to retrieve. The system will return an `ImageDetail` model object that includes prompt, filename and guid.

4. Retrieve Image Content: This use case involves retrieving the content of an image by its GUID. The user must provide the GUID of the image they wish to retrieve. The system will return the image bytes in the body of the HTTP response.
