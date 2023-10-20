from unittest import TestCase, mock
from unittest.mock import MagicMock, Mock
from person.application.use_cases import SavePersonUseCase, SearchPersonUseCase
from person.domain.model import Person
from person.infrastructure.mongo_repository import MongoPersonRepository


class GetPersonIdUseCaseTestCase(TestCase):
    def setUp(self) -> None:
        self._repository = MagicMock(MongoPersonRepository)
        self._sut = SearchPersonUseCase(repository=self._repository)

    def test_get_person_id(self):
        self._repository.get_person_id.return_value = None
        fixture_a = Person('a', 'a')
        fixture_b = Person('b', 'b')
        fixture_c = Person('c', 'c')
        fixture_d = Person('d', 'd', fixture_a, fixture_b, fixture_c)

        self._sut.get_person_id(fixture_d)
        self._repository.get_person_id.assert_has_calls(
            [mock.call(fixture_a, None, None, None),
             mock.call(fixture_b, None, None, None),
             mock.call(fixture_c, None, None, None),
             mock.call(fixture_d, None, None, None)]
        )


class SavePersonTestCase(TestCase):
    def setUp(self) -> None:
        self._repository = MagicMock(MongoPersonRepository)
        self._sut = SavePersonUseCase(repository=self._repository)

    def test_save_existing(self):
        self._repository.get_person_id = Mock(
            return_value='test'
        )

        self.assertEqual('test', self._sut.save_person(Person('test',
                                                              'test')))

    def test_save_new(self):
        self._repository.get_person_id = Mock(
            return_value=None
        )

        fixture_a = Person('a', 'a')
        fixture_b = Person('b', 'b')
        fixture_c = Person('c', 'c')
        fixture_d = Person('d', 'd', fixture_a, fixture_b, fixture_c)

        self._sut.save_person(fixture_d)
        self._repository.save_person.assert_has_calls(
            [mock.call(fixture_a), mock.call(fixture_b),
             mock.call(fixture_c), mock.call(fixture_d)]
        )
