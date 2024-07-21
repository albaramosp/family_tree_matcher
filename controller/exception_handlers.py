import traceback

from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from controller.logging_handler import LoggingHandler
from person.public.exception import MalformedRequestException


async def person_not_exists_exception_handler(request: Request, exc: MalformedRequestException):
    return JSONResponse(
        status_code=400,
        content={"message": repr(exc)},
    )


def handle_exception(req, exc):
    logging_handler = LoggingHandler()
    logger = logging_handler.get_logger()
    logger.error(traceback.format_exception(exc))
    return Response("Internal Server Error",
                    status_code=500)
