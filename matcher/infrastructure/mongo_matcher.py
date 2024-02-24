import abc
from typing import List

from person.application.driven.ports import PersonRepository
from matcher.application.driven.ports import MatcherManager
from settings.environment import get_environment


class SiblingMatcher(abc.ABC):
    @abc.abstractmethod
    def search_siblings(self, person_id: str, siblings: list):
        ...


class LeftSiblingMatcher(SiblingMatcher):
    def __init__(self, collection, person_repository: PersonRepository):
        self.collection = collection
        self.person_repository = person_repository

    def search_siblings(self,
                        person_id: str,
                        siblings: list):
        if person_id is None:
            return
        else:
            people = self.collection.find({
                'right_sibling': person_id
            })

            if people:
                for person in people:
                    parsed_person = self.person_repository.person_from_mongo_instance(person)
                    siblings.append(parsed_person)
                    self.search_siblings(
                        person_id=person.get('_id'),
                        siblings=siblings)


class RightSiblingMatcher(SiblingMatcher):
    def __init__(self, collection, person_repository: PersonRepository):
        self.collection = collection
        self.person_repository = person_repository

    def search_siblings(self,
                        person_id: str,
                        siblings: list):
        if person_id is None:
            return
        else:
            people = self.collection.find({
                '_id': person_id
            })

            if people:
                for person in people:
                    parsed_person = self.person_repository.person_from_mongo_instance(person)
                    siblings.append(parsed_person)
                    self.search_siblings(
                        person_id=person.get('right_sibling'),
                        siblings=siblings)


class MongoMatcher(MatcherManager):
    def __init__(self, person_repository):
        self.person_repository = person_repository
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

    def match_siblings(self, person_id: str) -> List[dict]:
        instance = self.collection.find_one({
            '_id': person_id
        })

        siblings = []

        LeftSiblingMatcher(self.collection,
                           self.person_repository).search_siblings(instance.get('_id'),
                                                                   siblings)
        RightSiblingMatcher(self.collection,
                            self.person_repository).search_siblings(instance.get('right_sibling'),
                                                                    siblings)

        return siblings
