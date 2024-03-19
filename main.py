import traceback

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from core.exceptions import ImageGenerationException, EXCEPTION_STATUS_CODES
from web.middleware import LoggingMiddleware, RequestIdMiddleware
from web.routers.image_router import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Register routers

# Include the router with a prefix
app.include_router(router)
# Innermost first
app.add_middleware(LoggingMiddleware)  # type: ignore
app.add_middleware(RequestIdMiddleware)  # type: ignore
# # Configure CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.exception_handler(ImageGenerationException)
async def handle_prompt_exception(_request: Request, exc: ImageGenerationException):
    # Get the status code from our mapping or default to 500 if not found
    status_code = EXCEPTION_STATUS_CODES.get(type(exc), 500)
    traceback_string = traceback.format_exc()
    return JSONResponse(status_code=status_code, content={"detail": str(exc), "traceback": traceback_string})


@app.exception_handler(Exception)
async def handle_generic_exception(_request: Request, exc: Exception):
    # Log the exception for debugging (optional)
    print(exc)
    return JSONResponse(status_code=500, content={"detail": "An unexpected error occurred."})
