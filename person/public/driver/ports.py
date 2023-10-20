from abc import ABC, abstractmethod
from person.public.entities import PersonOperationResponseDto, PersonDto


class PersonManager(ABC):
    @abstractmethod
    def handle_save(self, rq: PersonDto) -> PersonOperationResponseDto:
        ...
