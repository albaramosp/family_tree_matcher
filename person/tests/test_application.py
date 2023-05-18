from unittest import TestCase
from unittest.mock import MagicMock, Mock
from person.application.use_cases import SavePersonUseCase
from person.domain.model import Person
from person.domain.driven.ports import PersonRepository


class PersonUseCaseTestCase(TestCase):
    def setUp(self) -> None:
        self.repository = MagicMock(PersonRepository)

    def test_save(self):
        sut = SavePersonUseCase(self.repository)
        sut.execute(Person(name="test", surname="test"))
        self.repository.save_person.assert_called_once()
        self.repository.save_person.assert_called_with(Person(name="test", surname="test"))
