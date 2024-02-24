from __future__ import annotations

from person.application.use_cases import SavePersonUseCase
from person.public.driver.ports import PersonManager
from person.domain.model import Person
from person.public.entities import PersonDto, AddParentRequestDto, PersonWithRelativesDto

from person.infrastructure.factory import DefaultPersonRepositoryFactory


class PersonAdapter(PersonManager):
    def __init__(self):
        self._use_case = SavePersonUseCase(DefaultPersonRepositoryFactory().create_person_repository())

    def handle_save(self, rq: PersonWithRelativesDto):
        self._use_case.save_person(person=person_with_relatives_from_dto(rq))

    def add_parent(self, rq: AddParentRequestDto):
        self._use_case.add_parent(parent=person_from_dto(rq.parent),
                                  child=person_from_dto(rq.child))


def person_to_dto(person: Person) -> PersonDto:
    return PersonDto(name=person.name,
                     surname=person.surname)


def person_from_dto(dto: PersonDto) -> Person:
    return Person(name=dto.name,
                  surname=dto.surname)


def person_with_relatives_from_dto(dto: PersonWithRelativesDto) -> Person:
    person = person_from_dto(dto)

    if dto.first_child:
        person.first_child = person_from_dto(dto.first_child)
    if dto.right_sibling:
        person.right_sibling = person_from_dto(dto.right_sibling)
    if dto.partner:
        person.partner = person_from_dto(dto.partner)

    return person
