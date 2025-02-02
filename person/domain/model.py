from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class Person:
    """
    Model representing a person with relatives

    Attributes:
        name (str): person's name
        surname (str): person's surname
        first_child (Person): person's first child, optional
        right_sibling (Person): person's right_sibling, optional
        partner (Person): person's partner, optional

    """
    name: str
    surname: str
    first_child: Optional[Person] = None
    right_sibling: Optional[Person] = None
    partner: Optional[Person] = None
    id: Optional[str] = None
