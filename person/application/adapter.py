from __future__ import annotations

from person.application.use_cases import SavePersonUseCase
from person.infrastructure.factory import create_mongo_person_repository
from person.public.driver.ports import PersonManager
from person.domain.model import Person
from person.public.entities import PersonDto, PersonOperationResponseDto


class PersonAdapter(PersonManager):
    def handle_save(self, rq: PersonDto) -> PersonOperationResponseDto:
        person = person_from_dto(rq)
        res = PersonOperationResponseDto()
        try:
            SavePersonUseCase(repository=create_mongo_person_repository()).save_person(person=person)
            res.person = rq
        except Exception as e:
            print("Exception: ", e)
            res.error = repr(e)
            res.error_code = 500

        return res


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
