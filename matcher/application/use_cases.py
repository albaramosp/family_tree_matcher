from abc import abstractmethod

from person.application.driven.ports import PersonRepository
from person.public.exception import MalformedRequestException
from person.domain.model import Person


class MatchSiblingsStrategy:
    @abstractmethod
    def _add_left_siblings(self, person_id,
                           siblings: list):
        ...

    @abstractmethod
    def _add_right_siblings(self, person_id,
                            siblings: list):
        ...

    def match_siblings_strategy(self, person_id) -> list:
        siblings = []

        self._add_left_siblings(person_id, siblings)
        self._add_right_siblings(person_id, siblings)

        return siblings


class MatcherUseCase(MatchSiblingsStrategy):
    def __init__(self, repository: PersonRepository):
        self._repository = repository

    def _add_left_siblings(self, person_id,
                           siblings: list):
        self._repository.search_left_siblings(person_id, siblings)

    def _add_right_siblings(self, person_id,
                            siblings: list):
        self._repository.search_right_siblings(person_id, siblings)

    def match_siblings(self, person: Person):
        person_id = self._repository.get_person_id(person)
        if not person_id:
            raise MalformedRequestException("Person does not exist")

        return self.match_siblings_strategy(person_id)
