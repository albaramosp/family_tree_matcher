from typing import Optional
from person.domain.model import Person
from person.application.driven.ports import PersonRepository
from settings.environment import get_environment


class MongoPersonRepository(PersonRepository):
    def __init__(self):
        self._set_database()

    def _set_database(self):
        env = get_environment()
        if env == "pro":
            from settings.pro import CLOUD_MONGO_CLIENT
            client = CLOUD_MONGO_CLIENT
        elif env == "test":
            from settings.test import CLOUD_MONGO_CLIENT
            client = CLOUD_MONGO_CLIENT
        else:
            raise Exception("Environment not set")

        self.client = client
        self.database = self.client['family_tree_matcher']
        self.collection = self.database['people']

    def person_to_mongo(self, person: Person) -> dict:
        query = {
            'name': person.name,
            'surname': person.surname
        }

        if person.first_child:
            query.update({
                'first_child': self.get_person_id(person.first_child)})
        if person.right_sibling:
            query.update({
                'right_sibling': self.get_person_id(person.right_sibling)})
        if person.partner:
            query.update({
                'partner': self.get_person_id(person.partner)})

        return query

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
            query.update({'first_child': first_child_id})
        if right_sibling_id:
            query.update({'right_sibling': right_sibling_id})
        if partner_id:
            query.update({'partner': partner_id})

        person = self.collection.find_one(query)

        return person['_id'] if person else None

    def find_person(self,
                    person: Person,
                    first_child_id: str = None,
                    right_sibling_id: str = None,
                    partner_id: str = None) -> Optional[Person]:
        query = {
            "name": person.name,
            "surname": person.surname
        }

        if first_child_id:
            query.update({'first_child': first_child_id})
        if right_sibling_id:
            query.update({'right_sibling': right_sibling_id})
        if partner_id:
            query.update({'partner': partner_id})

        doc = self.collection.find_one(query)

        return (doc['_id'], self.person_from_mongo_instance(doc)) if doc else None

    def save_person(self, person: Person) -> str:
        query = self.person_to_mongo(person)

        return self.collection.insert_one(query).inserted_id

    def update_person(self, person_id: str, person: Person):
        query = self.person_to_mongo(person)
        self.collection.update_one({'_id': person_id},
                                   {'$set': query})
