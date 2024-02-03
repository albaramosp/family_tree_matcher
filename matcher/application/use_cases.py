from matcher.application.driven.ports import MatcherManager
from person.application.driven.ports import PersonRepository
from person.public.exception import MalformedRequestException
from person.domain.model import Person


class MatcherUseCase:
    def __init__(self, manager: MatcherManager, repository: PersonRepository):
        self.manager = manager
        self.person_repository = repository

    def match_siblings(self, person: Person):
        person_id = self.person_repository.get_person_id(Person(name=person.name,
                                                                surname=person.surname))
        if not person_id:
            raise MalformedRequestException("Person does not exist")
        return self.manager.match_siblings(person_id)
