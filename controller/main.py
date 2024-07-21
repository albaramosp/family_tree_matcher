from typing import Callable

import uvicorn
from fastapi import FastAPI, Request, APIRouter, Response
from fastapi.routing import APIRoute
from starlette.background import BackgroundTask
from starlette.responses import StreamingResponse

from controller.exception_handlers import person_not_exists_exception_handler, handle_exception
from controller.logging_handler import LoggingHandler
from matcher.public.driver.factory import get_manager as create_matcher_adapter

from person.public.exception import MalformedRequestException
from person.public.entities import PersonDto, AddParentRequestDto, PersonWithRelativesDto
from person.public.driver.factory import get_manager as create_person_adapter
from settings.environment import set_environment

logging_handler = LoggingHandler()
logger = logging_handler.get_logger()
set_environment("pro")


class LoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            req_body = await request.body()
            response = await original_route_handler(request)
            tasks = response.background

            if isinstance(response, StreamingResponse):
                res_body = b''
                async for item in response.body_iterator:
                    res_body += item

                task = BackgroundTask(logging_handler.log_info, request, req_body)
                response = Response(content=res_body, status_code=response.status_code,
                                    headers=dict(response.headers), media_type=response.media_type)
            else:
                task = BackgroundTask(logging_handler.log_info, request, req_body)

            # check if the original response had background tasks already attached to it
            if tasks:
                tasks.add_task(task)  # add the new task to the tasks list
                response.background = tasks
            else:
                response.background = task

            return response

        return custom_route_handler


app = FastAPI()
app.add_exception_handler(MalformedRequestException, person_not_exists_exception_handler)
app.add_exception_handler(Exception, handle_exception)
router = APIRouter(route_class=LoggingRoute)


@router.post("/person/save/")
def save_person(request: PersonWithRelativesDto):
    result = create_person_adapter().handle_save(request)
    return result


@app.post("/person/add_parent/")
def add_parent(request: AddParentRequestDto):
    result = create_person_adapter().add_parent(request)
    return result


@router.post("/matcher/match_siblings/")
def match_person_siblings(request: PersonDto) -> list[PersonDto]:
    return create_matcher_adapter().match_siblings(request)


app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
