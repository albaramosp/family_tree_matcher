from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class Person:
    name: str
    surname: str
    first_child: Optional[Person] = None
    right_sibling: Optional[Person] = None
    partner: Optional[Person] = None
