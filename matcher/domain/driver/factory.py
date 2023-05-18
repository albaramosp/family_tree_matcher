from typing import List

from matcher.application.use_cases import MatchSiblingsUseCase
from matcher.domain.driver.ports import MatcherManager
from matcher.infrastructure.factory import create_mongo_matcher_manager
from person.domain.model import PersonDto, person_from_dto, person_to_dto
from person.infrastructure.factory import create_mongo_person_repository


def get_manager() -> MatcherManager:
    return DefaultManager()


class DefaultManager(MatcherManager):
    def handle_match_siblings(self, rq: PersonDto) -> List[PersonDto]:
        person = person_from_dto(rq)
        matches = MatchSiblingsUseCase(
            manager=create_mongo_matcher_manager(),
            repository=create_mongo_person_repository()).execute(person=person)

        return [person_to_dto(person) for person in matches] \
            if matches else []
