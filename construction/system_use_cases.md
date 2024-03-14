Here are the system use cases for the image generation system:

1. Generate an Image. This use case involves generating a new image and image detail from a prompt. The user must provide a prompt for generating the image. The system will generate a GUID for the image and store it in the database. The system will return the `ImageDetail` object that includes prompt, filename and guid of the newly generated image.

2. List all Images: This use case involves retrieving all images details for all images. The system will return a list of `ImageDetail` model object that includes prompt, filename and guid.

3. Get an Image: This use case involves retrieving image details for an image by its GUID. The user must provide the GUID of the image they wish to retrieve. The system will return an `ImageDetail` model object that includes prompt, filename and guid.

4. Get the Content of an Image: This use case involves retrieving the content of an image by its GUID. The user must provide the GUID of the prompt they wish to retrieve. The system will return the image bytes in the body of the HTTP response.
