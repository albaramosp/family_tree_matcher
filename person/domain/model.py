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


class PersonOperationRequestDto(BaseModel):
    name: str = None
    surname: str = None
    first_child: Optional[PersonOperationRequestDto] = None
    partner: Optional[PersonOperationRequestDto] = None
    right_sibling: Optional[PersonOperationRequestDto] = None


class PersonOperationResponseDto(BaseModel):
    error_code: int = None
    error: str = None
    person: Optional[PersonOperationRequestDto] = None


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
