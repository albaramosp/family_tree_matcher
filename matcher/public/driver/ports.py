from abc import ABC, abstractmethod
from typing import List

from person.public.entities import PersonDto


class MatcherManager(ABC):
    @abstractmethod
    def match_siblings(self, rq: PersonDto) -> List[PersonDto]:
        ...

    @abstractmethod
    def match_parents(self, rq: PersonDto) -> List[PersonDto]:
        ...
