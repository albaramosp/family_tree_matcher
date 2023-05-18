from abc import ABC, abstractmethod
from typing import List

from person.domain.model import PersonOperationRequestDto


class MatcherManager(ABC):
    @abstractmethod
    def handle_match_siblings(self, rq: PersonOperationRequestDto) -> List[PersonOperationRequestDto]:
        ...
