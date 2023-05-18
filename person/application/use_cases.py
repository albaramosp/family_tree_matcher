from typing import Optional

from person.domain.model import Person
from person.domain.driven.ports import PersonRepository


class PersonUseCase:
    def __init__(self, repository: PersonRepository):
        self.repository = repository


class SearchPersonUseCase(PersonUseCase):
    def get_person_id(self, person: Person) -> Optional[str]:
        first_child_id, right_sibling_id, partner_id = None, None, None

        if person.first_child:
            first_child_id = self.get_person_id(person.first_child)
        if person.right_sibling:
            right_sibling_id = self.get_person_id(person.right_sibling)
        if person.partner:
            partner_id = self.get_person_id(person.partner)

        return self.repository.get_person_id(
                      person,
                      first_child_id,
                      right_sibling_id,
                      partner_id)


class SavePersonUseCase(PersonUseCase):
    def save_person(self, person: Person):
        first_child_id = right_sibling_id = partner_id = None

        if person.first_child:
            first_child_id = self.save_person(person.first_child)
            person.first_child = first_child_id
        if person.right_sibling:
            right_sibling_id = self.save_person(person.right_sibling)
            person.right_sibling = right_sibling_id
        if person.partner:
            partner_id = self.save_person(person.partner)
            person.partner = partner_id

        person_id = self.repository.get_person_id(
                      person,
                      first_child_id,
                      right_sibling_id,
                      partner_id)

        return person_id if person_id else self.repository.save_person(person)
