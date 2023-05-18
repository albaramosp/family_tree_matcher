from typing import Optional
from person.domain.model import Person
from person.domain.driven.ports import PersonRepository


class MongoPersonRepository(PersonRepository):
    def __init__(self, client):
        self.client = client
        self.database = self.client['family_tree_matcher']
        self.collection = self.database['people']

    @staticmethod
    def person_to_mongo(person: Person) -> dict:
        return {
            'name': person.name,
            'surname': person.surname,
            'first_child': person.first_child,
            'right_sibling': person.right_sibling,
            'partner': person.partner
        }

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

    def get_person_id(self,
                      person: Person,
                      first_child_id: str = None,
                      right_sibling_id: str = None,
                      partner_id: str = None) -> Optional[str]:
        query = {
            "name": person.name,
            "surname": person.surname
        }

        if first_child_id:
            query.update({'first_child_id': first_child_id})
        if right_sibling_id:
            query.update({'right_sibling_id': right_sibling_id})
        if partner_id:
            query.update({'partner_id': partner_id})

        person = self.collection.find_one(query)

        return person['_id'] if person else None

    def save_person(self, person: Person) -> str:
        query = self.person_to_mongo(person)

        return self.collection.insert_one(query).inserted_id
