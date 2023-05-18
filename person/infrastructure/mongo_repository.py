from typing import Optional
from person.domain.model import Person
from person.domain.driven.ports import PersonRepository


class MongoPersonRepository(PersonRepository):
    def __init__(self, client):
        self.client = client
        self.database = self.client['family_tree_matcher']
        self.collection = self.database['people']

    def person_from_mongo_instance(self, instance: dict) -> Person:
        first_child = right_sibling = partner = None
        if instance.get('first_child'):
            person = self.collection.find_one({
                '_id': instance['first_child']
            })
            if person:
                first_child = self.person_from_mongo_instance(person)
        if instance.get('right_sibling'):
            person = self.collection.find_one({
                '_id': instance['right_sibling']
            })
            if person:
                right_sibling = self.person_from_mongo_instance(person)
        if instance.get('partner'):
            person = self.collection.find_one({
                '_id': instance['partner']
            })
            if person:
                partner = self.person_from_mongo_instance(person)

        return Person(name=instance['name'],
                      surname=instance['surname'],
                      first_child=first_child,
                      partner=partner,
                      right_sibling=right_sibling)

    def get_person_id(self, person: Person) -> Optional[str]:
        first_child_id, right_sibling_id, partner_id = self._get_relatives_ids(person)

        query = {
            "name": person.name,
            "surname": person.surname,
            "first_child": None,
            "right_sibling": None,
            "partner": None
        }

        if person.first_child:
            query["first_child"] = first_child_id
        if person.right_sibling:
            query["right_sibling"] = right_sibling_id
        if person.partner:
            query["partner"] = partner_id

        existing_person = self.collection.find_one(query)
        person_id = None
        if existing_person:
            person_id = existing_person['_id']

        return person_id

    def _get_relatives_ids(self, person: Person) -> (Optional[str],
                                                     Optional[str],
                                                     Optional[str]):
        first_child_id = right_sibling_id = partner_id = None
        if person.first_child:
            first_child_id = self.get_person_id(person.first_child)
        if person.right_sibling:
            right_sibling_id = self.get_person_id(person.right_sibling)
        if person.partner:
            partner_id = self.get_person_id(person.partner)

        return first_child_id, right_sibling_id, partner_id

    def save_person(self, person: Person) -> str:
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
            first_child_id = self.save_person(person.first_child)
        if person.right_sibling:
            right_sibling_id = self.save_person(person.right_sibling)
        if person.partner:
            partner_id = self.save_person(person.partner)

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
