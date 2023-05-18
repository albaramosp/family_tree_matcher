from abc import ABC, abstractmethod

from person.domain.model import Person


class PersonRepository(ABC):
    @abstractmethod
    def save_person(self, person: Person):
        ...


class PersonAlreadyExistsException(Exception):
    ...


class IncorrectPersonException(Exception):
    ...


class NonExistingPerson(Exception):
    ...
