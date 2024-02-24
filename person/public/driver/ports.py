from abc import ABC, abstractmethod
from person.public.entities import AddParentRequestDto, PersonWithRelativesDto


class PersonManager(ABC):
    @abstractmethod
    def handle_save(self, rq: PersonWithRelativesDto):
        ...

    @abstractmethod
    def add_parent(self, rq: AddParentRequestDto):
        ...
