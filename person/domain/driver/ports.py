from abc import ABC, abstractmethod
from person.domain.model import PersonOperationRequestDto, PersonOperationResponseDto


class PersonManager(ABC):
    @abstractmethod
    def handle_save(self, rq: PersonOperationRequestDto) -> PersonOperationResponseDto:
        ...
