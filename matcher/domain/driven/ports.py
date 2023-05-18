from abc import ABC, abstractmethod

from person.domain.driven.ports import PersonRepository
from person.domain.model import Person


class MatcherManager(ABC):
    @abstractmethod
    def match_siblings(self, person_id: str):
        ...

