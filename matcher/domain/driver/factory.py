from typing import List

from matcher.application.use_cases import MatchSiblingsUseCase
from matcher.domain.driver.ports import MatcherManager
from matcher.infrastructure.factory import create_mongo_matcher_manager
from person.domain.model import PersonOperationRequestDto, person_from_dto, person_to_dto


def get_manager() -> MatcherManager:
    return DefaultManager()


class DefaultManager(MatcherManager):
    def handle_match_siblings(self, rq: PersonOperationRequestDto) -> List[PersonOperationRequestDto]:
        person = person_from_dto(rq)

        matches = MatchSiblingsUseCase(manager=create_mongo_matcher_manager()).execute(person=person)
        parsed_matches = []
        if matches:
            for person in matches:
                parsed_matches.append(person_to_dto(person))

        return parsed_matches
