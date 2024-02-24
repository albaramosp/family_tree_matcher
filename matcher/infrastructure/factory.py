import abc
from matcher.application.driven.ports import MatcherManager
from matcher.infrastructure.mongo_matcher import MongoMatcher
from person.infrastructure.factory import DefaultPersonRepositoryFactory


class MatcherManagerFactory(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def create_matcher_manager() -> MatcherManager:
        ...


class DefaultMatcherManagerFactory(MatcherManagerFactory):
    def __init__(self):
        self.manager = None

    def create_matcher_manager(self) -> MatcherManager:
        if not self.manager:
            self.manager = MongoMatcher(
                person_repository=DefaultPersonRepositoryFactory().create_person_repository())
        return self.manager
