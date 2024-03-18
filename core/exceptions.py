# Define custom exceptions for error conditions in the data layer
# Ensure that these exceptions extend a base exception class, like ImageGenerationException
class ImageGenerationException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class DBConnectionError(ImageGenerationException):
    def __init__(self, message="Failed to connect to the database."):
        super().__init__(message)


class RecordNotFoundError(ImageGenerationException):
    def __init__(self, message="The requested record was not found."):
        super().__init__(message)


class ConstraintViolationError(ImageGenerationException):
    def __init__(self, message="Database constraint was violated."):
        super().__init__(message)

# 2. Service Layer Exceptions
        
# 3. Web Layer Exceptions
class BadRequestError(ImageGenerationException):
    def __init__(self, message="Bad request data."):
        super().__init__(message)


class EndpointNotFoundError(ImageGenerationException):
    def __init__(self, message="Endpoint not found."):
        super().__init__(message)

EXCEPTION_STATUS_CODES = {
    # DataValidationError: 400,       # Bad Request
    ConstraintViolationError: 409,  # Conflict
    ImageGenerationException: 500,           # Internal Server Error (Generic fallback)
    DBConnectionError: 500,         # Internal Server Error (Generic fallback)
    RecordNotFoundError: 404,       # Not Found
    # UnauthorizedError: 401,         # Unauthorized
    # OperationNotAllowedError: 403,  # Forbidden
    BadRequestError: 400,           # Bad Request
    EndpointNotFoundError: 404,     # Not Found
    # AuthenticationError: 401,       # Unauthorized
}