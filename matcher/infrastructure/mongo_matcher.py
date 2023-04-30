from person.domain.model import Person
from matcher.matcher_interfaces import AbstractMatcher


class MongoMatcher(AbstractMatcher):
    def __init__(self, client):
        self.client = client
        self.database = self.client['family_tree_matcher']
        self.collection = self.database['people']

    def match(self, person: Person) -> list:
        match = []

        brothers = self._get_person_siblings(person)

        # TODO match other type of relationships

        if len(brothers) > 0:
            match = brothers

        return match

    # TODO an observer pattern to update people when a family member is created
    # TODO en matcher?
    def _recursive_sibling_search(self, person_id: str):
        if person_id is None:
            return []
        else:
            result = self._recursive_sibling_search(self.collection.find_one({
                '_id': person_id
            },
                {'right_sibling': 1})[0]['right_sibling'])
            result.append(person_id)
            return result

    def _get_person_siblings(self, person: Person) -> list:
        # Get & store right sibling until no more siblings are found
        instance = self.collection.find_one({
            'name': person.name,
            'surname': person.surname,
            'partner': person.partner,
            'first_child': person.first_child,
            'right_sibling': person.right_sibling
        }, {'_id': 1})
        if instance:
            person_id = instance[0]['_id']
            res = self._recursive_sibling_search(person_id)
            print(res)
        return []
