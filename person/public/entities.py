from __future__ import annotations
from typing import Optional
from dataclasses import dataclass

from pydantic import BaseModel


# Model should inherit from BaseModel in order to reference itself
class PersonDto(BaseModel):
    name: str
    surname: str
    first_child: Optional[PersonDto] = None
    partner: Optional[PersonDto] = None
    right_sibling: Optional[PersonDto] = None


class AddParentRequestDto(BaseModel):
    parent: PersonDto
    child: PersonDto
