import abc
from abc import ABC
from typing import Optional

from person.domain.model import Person


class PersonRepository(ABC):
    @abc.abstractmethod
    def get_person_id(self,
                      person: Person,
                      first_child_id: str = None,
                      right_sibling_id: str = None,
                      partner_id: str = None) -> Optional[str]:
        ...

    @abc.abstractmethod
    def find_person(self,
                    person: Person,
                    first_child_id: str = None,
                    right_sibling_id: str = None,
                    partner_id: str = None) -> Optional[tuple[str, Person]]:
        ...

    @abc.abstractmethod
    def save_person(self, person: Person) -> str:
        ...

    @abc.abstractmethod
    def update_person(self, person_id: str, person: Person):
        ...

    @abc.abstractmethod
    def search_right_siblings(self,
                              person_id: str,
                              siblings: list):
        ...

    @abc.abstractmethod
    def search_left_siblings(self,
                             person_id: str,
                             siblings: list):
        ...
