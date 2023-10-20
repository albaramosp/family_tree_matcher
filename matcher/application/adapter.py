from typing import List

from matcher.application.use_cases import MatchSiblingsUseCase
from matcher.infrastructure.factory import create_mongo_matcher_manager
from matcher.public.driver.ports import MatcherManager
from person.application.adapter import person_from_dto, person_to_dto
from person.infrastructure.factory import create_mongo_person_repository
from person.public.entities import PersonDto


class MatcherAdapter(MatcherManager):
    def handle_match_siblings(self, rq: PersonDto) -> List[PersonDto]:
        person = person_from_dto(rq)
        matches = MatchSiblingsUseCase(
            manager=create_mongo_matcher_manager(),
            repository=create_mongo_person_repository()).execute(person=person)

        return [person_to_dto(person) for person in matches] \
            if matches else []
