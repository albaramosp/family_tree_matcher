from __future__ import annotations
from abc import ABC
from dataclasses import dataclass
from typing import Optional


@dataclass
class Person:
    name: str
    surname: str
    first_child: Optional[Person] = None
    right_sibling: Optional[Person] = None
    partner: Optional[Person] = None
    id: Optional[str] = None


class PersonRepository(ABC):
    def serialize(self, person: Person):
        ...

    def save(self, person: Person):
        ...


class PersonAlreadyExists(Exception):
    ...


class IncorrectPerson(Exception):
    ...


class MongoPersonRepository(PersonRepository):
    def __init__(self, client):
        self.client = client
        self.database = self.client['family_tree_matcher']
        self.collection = self.database['people']

    # TODO I may not need this
    def serialize(self, person: Person) -> dict:
        """
        Transform a person object into a dictionary. The
        relatives of the person are stored as references.
        :param person: Person object
        :return: dictionary with person's properties
        """
        if not person.name or not person.surname:
            raise IncorrectPerson("Person must have name and surname")

        result = {
            "name": person.name,
            "surname": person.surname,
        }

        # Relatives are stored as references
        if person.first_child:
            result["first_child"] = person.first_child.id
        if person.right_sibling:
            result["right_sibling"] = person.right_sibling.id
        if person.partner:
            result["partner"] = person.partner.id

        return result

    def save(self, person: Person) -> str:
        """
        Save a person and its relatives into the database,
        returning the id of the inserted person. If the person
        is already registered, its id will be returned.

        :param person: Person to be registered
        :return: id of the registered person
        """
        first_child_id, right_sibling_id, partner_id = self._save_relatives(person)

        self._update_person_relatives(person,
                                      first_child_id,
                                      right_sibling_id,
                                      partner_id)

        return self._get_or_create(person)

    def _get_or_create(self, person: Person) -> str:
        """
        Retrieve a person if it's already registered in the database
        by checking if any other person with the same name and
        family structure exists, or create it if it is not registered.

        :param person: person to check its existence

        :return: registered person's database id
        """
        query = {
            "name": person.name,
            "surname": person.surname,
            "first_child": None,
            "right_sibling": None,
            "partner": None
        }

        if person.first_child:
            query["first_child"] = person.first_child.id
        if person.right_sibling:
            query["right_sibling"] = person.right_sibling.id
        if person.partner:
            query["partner"] = person.partner.id

        existing_person = self.collection.find_one(query)
        if existing_person:
            return existing_person['_id']

        return self.collection.insert_one(query).inserted_id

    def _save_relatives(self, person: Person) -> (Optional[str], Optional[str], Optional[str]):
        """
        Save a person's relatives into the database
        :param person: Person whose relatives are to be stored
        :return: triple with first child, right sibling and partner's ids
        """
        first_child_id = right_sibling_id = partner_id = None
        if person.first_child:
            first_child_id = self.save(person.first_child)
        if person.right_sibling:
            right_sibling_id = self.save(person.right_sibling)
        if person.partner:
            partner_id = self.save(person.partner)

        return first_child_id, right_sibling_id, partner_id

    def _update_person_relatives(self,
                                 person: Person,
                                 first_child_id: Optional[str],
                                 right_sibling_id: Optional[str],
                                 partner_id: Optional[str]):
        """
        Updates the references of a person's relatives after
        they've been registered in the database.
        :param person: Person to be updated
        :param first_child_id: database reference to the first child
        :param right_sibling_id: database reference to the right sibling
        :param partner_id: database reference to the partner
        """
        if person.first_child:
            person.first_child.id = first_child_id
            self.collection.update_one({
                "_id": person.first_child.id
            }, {
                "$set": {"_id": person.first_child.id}
            })
        if person.right_sibling:
            person.right_sibling.id = right_sibling_id
            self.collection.update_one({
                "_id": person.right_sibling.id
            }, {
                "$set": {"_id": person.right_sibling.id}
            })
        if person.partner:
            person.partner.id = partner_id
            self.collection.update_one({
                "_id": person.partner.id
            }, {"$set": {
                "_id": person.partner.id}})
