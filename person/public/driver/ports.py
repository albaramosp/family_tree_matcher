from abc import ABC, abstractmethod
from person.public.entities import PersonDto, AddParentRequestDto


class PersonManager(ABC):
    @abstractmethod
    def handle_save(self, rq: PersonDto):
        ...

    @abstractmethod
    def add_parent(self, rq: AddParentRequestDto):
        ...
