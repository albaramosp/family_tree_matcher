from typing import Optional, List
import uvicorn
from fastapi import FastAPI

from controller.adapters import PersonAdapter, MatcherAdapter
from controller.exception_handlers import person_not_exists_exception_handler

from person.domain.driven.ports import NonExistingPerson
from person.domain.model import PersonOperationRequestDto, PersonOperationResponseDto

app = FastAPI()
app.add_exception_handler(NonExistingPerson, person_not_exists_exception_handler)


@app.post("/person/save/")
def save_person(name: str,
                surname: str,
                first_child: Optional[PersonOperationRequestDto] = None,
                partner: Optional[PersonOperationRequestDto] = None,
                right_sibling: Optional[PersonOperationRequestDto] = None) -> PersonOperationResponseDto:
    dto = PersonOperationRequestDto()
    dto.name = name
    dto.surname = surname
    dto.first_child = first_child
    dto.partner = partner
    dto.right_sibling = right_sibling

    result = PersonAdapter().handle_save(dto)
    return result


@app.get("/matcher/match_siblings/")
def match_person_siblings(name: str,
                          surname: str,
                          first_child: Optional[PersonOperationRequestDto] = None,
                          partner: Optional[PersonOperationRequestDto] = None,
                          right_sibling: Optional[PersonOperationRequestDto] = None) -> List[PersonOperationRequestDto]:
    # TODO optional parameters in body, not supported by GETs
    dto = PersonOperationRequestDto()
    dto.name = name
    dto.surname = surname
    dto.first_child = first_child
    dto.partner = partner
    dto.right_sibling = right_sibling

    return MatcherAdapter().handle_match_siblings(dto)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
