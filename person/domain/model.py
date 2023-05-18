from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel


@dataclass
class Person:
    name: str
    surname: str
    first_child: Optional[Person] = None
    right_sibling: Optional[Person] = None
    partner: Optional[Person] = None
    id: Optional[str] = None


class PersonDto(BaseModel):
    name: str
    surname: str
    first_child: Optional[PersonDto] = None
    partner: Optional[PersonDto] = None
    right_sibling: Optional[PersonDto] = None


class PersonOperationResponseDto(BaseModel):
    error_code: int = None
    error: str = None
    person: Optional[PersonDto] = None


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
def person_to_dto(person: Person) -> PersonOperationRequestDto:
    first_child = right_sibling = partner = None
    if person.first_child:
        first_child = person_to_dto(person.first_child)
    if person.right_sibling:
        right_sibling = person_to_dto(person.right_sibling)
    if person.partner:
        partner = person_to_dto(person.partner)

    dto = PersonOperationRequestDto()
    dto.name = person.name
    dto.surname = person.surname
    dto.first_child = first_child
    dto.partner = partner
    dto.right_sibling = right_sibling

    return dto

def person_from_dto(dto: PersonOperationRequestDto) -> Person:
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
