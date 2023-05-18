from typing import Optional
import uvicorn
from fastapi import FastAPI

from matcher.domain.driver.factory import get_manager as get_matcher_manager
from matcher.domain.driver.ports import MatcherManager
from matcher.domain.model import MatcherOperationResponseDto

from person.domain.driver.factory import get_manager as get_person_manager
from person.domain.driver.ports import PersonManager
from person.domain.model import PersonOperationRequestDto, PersonOperationResponseDto

app = FastAPI()


class PersonAdapter(PersonManager):
    def handle_save(self, rq: PersonOperationRequestDto) -> PersonOperationResponseDto:
        return get_person_manager().handle_save(rq)


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


class MatcherAdapter(MatcherManager):
    def handle_match_siblings(self, rq: PersonOperationRequestDto) -> MatcherOperationResponseDto:
        return get_matcher_manager().handle_match_siblings(rq)


@app.get("/matcher/match_siblings/")
def match_person_siblings(name: str,
                          surname: str,
                          first_child: Optional[PersonOperationRequestDto] = None,
                          partner: Optional[PersonOperationRequestDto] = None,
                          right_sibling: Optional[PersonOperationRequestDto] = None) -> MatcherOperationResponseDto:
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
