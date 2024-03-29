import abc

from person.application.driven.ports import PersonRepository
from person.infrastructure.mongo_repository import MongoPersonRepository


class PersonRepositoryFactory(abc.ABC):
    @abc.abstractmethod
    def create_person_repository(self) -> PersonRepository:
        ...


class DefaultPersonRepositoryFactory(PersonRepositoryFactory):
    def __init__(self):
        self.repository = None

    def create_person_repository(self) -> PersonRepository:
        if not self.repository:
            self.repository = MongoPersonRepository()
        return self.repository
