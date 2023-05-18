from abc import ABC, abstractmethod
from typing import List

from person.domain.model import PersonDto


class MatcherManager(ABC):
    @abstractmethod
    def handle_match_siblings(self, rq: PersonDto) -> List[PersonDto]:
        ...
