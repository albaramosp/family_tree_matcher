from starlette.requests import Request
from starlette.responses import JSONResponse

from person.domain.driven.ports import NonExistingPerson


async def person_not_exists_exception_handler(request: Request, exc: NonExistingPerson):
    return JSONResponse(
        status_code=404,
        content={"message": repr(exc)},
    )
