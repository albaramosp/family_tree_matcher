from person.domain.model import Person
from person.domain.driven.ports import PersonRepository


class PersonUseCase:
    def __init__(self, repository: PersonRepository):
        self.repository = repository


class SavePersonUseCase(PersonUseCase):
    def execute(self, person: Person):
        self.repository.save_person(person)
