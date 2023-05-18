from typing import List
import uvicorn
from fastapi import FastAPI

from controller.adapters import PersonAdapter, MatcherAdapter
from controller.exception_handlers import person_not_exists_exception_handler

from person.domain.driven.ports import MalformedRequestException
from person.domain.model import PersonDto, PersonOperationResponseDto

app = FastAPI()
app.add_exception_handler(MalformedRequestException, person_not_exists_exception_handler)


@app.post("/person/save/")
def save_person(request: PersonDto) -> PersonOperationResponseDto:
    result = PersonAdapter().handle_save(request)
    return result


@app.post("/matcher/match_siblings/")
def match_person_siblings(request: PersonDto) -> List[PersonDto]:

    return MatcherAdapter().handle_match_siblings(request)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
