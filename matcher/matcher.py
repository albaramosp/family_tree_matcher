from interfaces.public import AbstractMatcher


class MongoMatcher(AbstractMatcher):
    def __init__(self, client):
        self.client = client
        self.database = self.client['family_tree_matcher']
        self.collection = self.database['people']

    def match(self, person: dict) -> list:
        match = []

        brothers = self._get_person_siblings(person)

        # TODO match other type of relationships

        if len(brothers) > 0:
            match = brothers

        return match

    # TODO an observer pattern to update people when a family member is created
