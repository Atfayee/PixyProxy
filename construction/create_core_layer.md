Lets build the core model layer for the following system and database schema.
The system description is as follows:

```
{system-description?}
```

Here is the database schema to use:

```
{schema-description?}
```

Let's make sure to cover the following use cases for our system:

```
{system-usecase-summary?}
```

For the content of the core layer, let's generate two files:

## core/models.py

Let's make sure that for each model object, say X, we have a class for the data items
it takes to make X (named class XCreate), and a class for the data items we need to display X
(named class X extending XCreate).

## core/exceptions.py

Let's make sure to have a custom exception for each error condition that can occur in the system.
Every exception should extend a class called ImageGenerationException that itself extends Exception.

For the data layer exceptions, let's generate:
class DBConnectionError(PromptException):

- a connection to the database could not be established

class RecordNotFoundError(PromptException):

- The requested record was not found."):

Make sure the exceptions can be raised with a message.
For example:
    class ImageGenerationException(Exception):
        def **init**(self, message: str):
            self.message = message
            super().**init**(self.message)

class ConstraintViolationError
- a database constraint was violated
