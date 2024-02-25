from typing import List

from matcher.application.use_cases import MatcherUseCase
from matcher.public.driver.ports import MatcherManager
from person.application.adapter import person_from_dto, person_to_dto
from person.infrastructure.factory import DefaultPersonRepositoryFactory
from person.public.entities import PersonDto


class MatcherAdapter(MatcherManager):
    def match_siblings(self, rq: PersonDto) -> List[PersonDto]:
        person = person_from_dto(rq)
        matches = MatcherUseCase(
            repository=DefaultPersonRepositoryFactory().create_person_repository()
        ).match_siblings(person=person)

        return [person_to_dto(person) for person in matches] \
            if matches else []

    def match_parents(self, rq: PersonDto) -> List[PersonDto]:
        pass
