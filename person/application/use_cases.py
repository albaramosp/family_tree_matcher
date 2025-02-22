from typing import Optional

from person.domain.model import Person
from person.application.driven.ports import PersonRepository


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
    def _get_or_create(self, person: Person) -> str:
        _id = self.repository.get_person_id(person)
        if not _id:
            _id = self.save_person(person)
        return _id

    def save_person(self, person: Person) -> str:
        """
        Register a person into the system

        :param person: person to register, with optional relatives
        :type person: Person
        :return: The id of the person registered
        :rtype: str
        """
        first_child_id = right_sibling_id = partner_id = None

        if person.first_child:
            first_child_id = self.save_person(person.first_child)
        if person.right_sibling:
            right_sibling_id = self.save_person(person.right_sibling)
        if person.partner:
            partner_id = self.save_person(person.partner)

        person_id = self.repository.get_person_id(
                      person,
                      first_child_id,
                      right_sibling_id,
                      partner_id)

        return person_id if person_id else self.repository.save_person(person)

    def add_partner(self, person: Person, partner: Person) -> str:
        db_person = self.repository.find_person(person)
        if db_person:
            person_id, stored_person = db_person
            stored_person.partner = partner
            self._get_or_create(partner)
            return self.repository.update_person(person_id, stored_person)
        else:
            person.partner = partner
            return self.repository.save_person(person)

    def add_parent(self, child: Person, parent: Person) -> str:
        db_parent = self.repository.find_person(parent)
        if db_parent:
            parent_id, stored_parent = db_parent

            if not stored_parent.first_child:
                parent.first_child = child
            else:
                child_id = self.repository.get_person_id(child)
                child.right_sibling = stored_parent.first_child
                if child_id:
                    self.repository.update_person(child_id, child)
                parent.first_child = child

            return self.repository.update_person(parent_id, parent)
        else:
            parent.first_child = child

        return self.repository.save_person(parent)
