from interfaces.public import AbstractMatcher
from person.person import Person


class PersonAlreadyExists(Exception):
    ...


class MongoMatcher(AbstractMatcher):
    def __init__(self, client):
        self.client = client
        self.database = self.client['family_tree_matcher']
        self.collection = self.database['people']

    def _check_person_exists(self, person: Person):
        # TODO modify this to check ancestors to determine if it's really the same person
        if self.collection.count_documents({
            'name': person.name,
            'surname': person.surname
        }) > 0:
            raise PersonAlreadyExists("A person with the same name is already registered")

    def _get_person_siblings(self, person: Person) -> list:
        # TODO check ancestors too
        return [x for x in self.collection.find({
            'surname': {
                '$regex': ' '.join(['(' + element + ')' for element in person.surname.split(' ')])
            }
        })]

    def match(self, person: Person) -> list:
        match = []
        if person.name and person.surname:
            self._check_person_exists(person)
            brothers = self._get_person_siblings(person)

            # TODO match other type of relationships

            if len(brothers) > 0:
                match = brothers

        return match

    # TODO a factory pattern to create people that don't exist in the DB?
    # TODO an observer pattern to update people when a family member is created

