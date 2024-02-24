from __future__ import annotations
from typing import Optional

from pydantic import BaseModel


# Model should inherit from BaseModel in order to reference itself
class PersonDto(BaseModel):
    name: str
    surname: str


class PersonWithRelativesDto(BaseModel):
    name: str
    surname: str
    first_child: Optional[PersonWithRelativesDto] = None
    partner: Optional[PersonWithRelativesDto] = None
    right_sibling: Optional[PersonWithRelativesDto] = None


class AddParentRequestDto(BaseModel):
    parent: PersonDto
    child: PersonDto
