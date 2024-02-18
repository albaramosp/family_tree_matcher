from abc import ABC
from typing import Optional

from person.domain.model import Person


class PersonRepository(ABC):
    def get_person_id(self,
                      person: Person,
                      first_child_id: str = None,
                      right_sibling_id: str = None,
                      partner_id: str = None) -> Optional[str]:
        ...

    def find_person(self,
                    person: Person,
                    first_child_id: str = None,
                    right_sibling_id: str = None,
                    partner_id: str = None) -> Optional[tuple[str, Person]]:
        ...

    def save_person(self, person: Person) -> str:
        ...

    def update_person(self, person_id: str, person: Person):
        ...
