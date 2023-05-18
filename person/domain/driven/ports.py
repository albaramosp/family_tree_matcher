from abc import ABC, abstractmethod
from typing import Optional

from person.domain.model import Person


class PersonRepository(ABC):
    @abstractmethod
    def get_person_id(self,
                      person: Person,
                      first_child_id: str = None,
                      right_sibling_id: str = None,
                      partner_id: str = None) -> Optional[str]:
        ...

    @abstractmethod
    def save_person(self, person: Person) -> str:
        ...


class MalformedRequestException(Exception):
    ...
