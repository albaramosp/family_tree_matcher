from starlette.requests import Request
from starlette.responses import JSONResponse

from person.public.exception import MalformedRequestException


async def person_not_exists_exception_handler(request: Request, exc: MalformedRequestException):
    return JSONResponse(
        status_code=400,
        content={"message": repr(exc)},
    )
