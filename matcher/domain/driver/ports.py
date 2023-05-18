from abc import ABC, abstractmethod

from matcher.domain.model import MatcherOperationResponseDto
from person.domain.model import PersonOperationRequestDto


class MatcherManager(ABC):
    @abstractmethod
    def handle_match_siblings(self, rq: PersonOperationRequestDto) -> MatcherOperationResponseDto:
        ...
