from __future__ import annotations

from person.application.use_cases import SavePersonUseCase
from person.infrastructure.factory import DefaultPersonRepositoryFactory
from person.public.driver.ports import PersonManager
from person.domain.model import Person
from person.public.entities import PersonDto, AddParentRequestDto


class PersonAdapter(PersonManager):
    def __init__(self):
        self._repository = DefaultPersonRepositoryFactory().create_person_repository()
        self._use_case = SavePersonUseCase(repository=self._repository)

    def handle_save(self, rq: PersonDto):
        self._use_case.save_person(person=person_from_dto(rq))

    def add_parent(self, rq: AddParentRequestDto):
        self._use_case.add_parent(parent=person_from_dto(rq.parent),
                                  child=person_from_dto(rq.child))


def person_to_dto(person: Person) -> PersonDto:
    dto = PersonDto(name=person.name,
                    surname=person.surname)
    if person.first_child:
        dto.first_child = person_to_dto(person.first_child)
    if person.right_sibling:
        dto.right_sibling = person_to_dto(person.right_sibling)
    if person.partner:
        dto.partner = person_to_dto(person.partner)

    return dto


def person_from_dto(dto: PersonDto) -> Person:
    first_child = right_sibling = partner = None
    if dto.first_child:
        first_child = person_from_dto(dto.first_child)
    if dto.right_sibling:
        right_sibling = person_from_dto(dto.right_sibling)
    if dto.partner:
        partner = person_from_dto(dto.partner)

    return Person(name=dto.name,
                  surname=dto.surname,
                  first_child=first_child,
                  partner=partner,
                  right_sibling=right_sibling)
