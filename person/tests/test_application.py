from unittest import TestCase
from unittest.mock import MagicMock, Mock
from person.application.use_cases import SavePersonUseCase, GetPersonUseCase
from person.domain.model import Person
from person.domain.driven.ports import PersonRepository


class PersonUseCaseTestCase(TestCase):
    def setUp(self) -> None:
        self.repository = MagicMock(PersonRepository)

    def test_save(self):
        sut = SavePersonUseCase(self.repository)
        sut.execute(Person(name="test", surname="test"))
        self.repository.save.assert_called_once()
        self.repository.save.assert_called_with(Person(name="test", surname="test"))

    def test_get_existing(self):
        sut = GetPersonUseCase(self.repository)
        self.repository.get = Mock(return_value=Person(name="test", surname="test"))
        obtained = sut.execute(person_id="test")
        self.assertEqual(obtained, Person(name="test", surname="test"))

