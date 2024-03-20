from fastapi import FastAPI, Request
from web.routers import images_routes
import traceback

from fastapi.responses import JSONResponse

from core.exceptions import PromptException, EXCEPTION_STATUS_CODES
# from web.middleware import LoggingMiddleware, RequestIdMiddleware

app = FastAPI()

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello, {name}"}

app.include_router(images_routes.router)
# app.include_router(images_routes.router, prefix="/image", tags=["Images"])


# Innermost first
# app.add_middleware(LoggingMiddleware)  # type: ignore
# app.add_middleware(RequestIdMiddleware)  # type: ignore


@app.exception_handler(PromptException)
async def handle_prompt_exception(_request: Request, exc: PromptException):
    # Get the status code from our mapping or default to 500 if not found
    status_code = EXCEPTION_STATUS_CODES.get(type(exc), 500)
    traceback_string = traceback.format_exc()
    return JSONResponse(status_code=status_code, content={"detail": str(exc), "traceback": traceback_string})


@app.exception_handler(Exception)
async def handle_generic_exception(_request: Request, exc: Exception):
    # Log the exception for debugging (optional)
    print(exc)
    return JSONResponse(status_code=500, content={"detail": "An unexpected error occurred."})