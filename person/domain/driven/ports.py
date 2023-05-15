from abc import ABC, abstractmethod

from person.domain.model import Person


class PersonRepository(ABC):
    @abstractmethod
    def save(self, person: Person):
        ...

    @abstractmethod
    def get(self, person_id: str) -> Person:
        ...


class PersonAlreadyExistsException(Exception):
    ...


class IncorrectPersonException(Exception):
    ...
