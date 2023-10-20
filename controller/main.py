import uvicorn
from fastapi import FastAPI

from matcher.application.adapter import MatcherAdapter
from controller.exception_handlers import person_not_exists_exception_handler

from person.public.exception import MalformedRequestException
from person.public.entities import PersonDto, PersonOperationResponseDto
from person.public.driver.factory import get_manager as create_person_manager

app = FastAPI()
app.add_exception_handler(MalformedRequestException, person_not_exists_exception_handler)


@app.post("/person/save/")
def save_person(request: PersonDto) -> PersonOperationResponseDto:
    result = create_person_manager().handle_save(request)
    return result


@app.post("/matcher/match_siblings/")
def match_person_siblings(request: PersonDto) -> list[PersonDto]:
    return MatcherAdapter().handle_match_siblings(request)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
