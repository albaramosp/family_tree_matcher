from abc import ABC, abstractmethod
from person.domain.model import PersonDto, PersonOperationResponseDto


class PersonManager(ABC):
    @abstractmethod
    def handle_save(self, rq: PersonDto) -> PersonOperationResponseDto:
        ...
