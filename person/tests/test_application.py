from copy import deepcopy
from unittest import TestCase, mock
from unittest.mock import MagicMock, Mock, call
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

    def test_add_non_stored_parent(self):
        fixture_parent = Person(name='test', surname='test')
        fixture_child = Person(name='test2', surname='test2')
        self._repository.find_person = Mock(return_value=None)
        self._sut.save_person = Mock()

        expected = deepcopy(fixture_parent)
        expected.first_child = fixture_child
        self._sut.add_parent(fixture_child, fixture_parent)
        self._repository.save_person.assert_called_with(expected)

    def test_add_parent_without_child(self):
        fixture_parent = Person(name='test', surname='test')
        fixture_child = Person(name='test2', surname='test2')
        self._repository.find_person = Mock(return_value=('test', fixture_parent))
        self._sut.save_person = Mock()

        expected = deepcopy(fixture_parent)
        expected.first_child = fixture_child
        self._sut.add_parent(fixture_child, fixture_parent)
        self._repository.update_person.assert_called_with('test',
                                                          expected)

    def test_add_parent_with_child(self):
        fixture_child = Person(name='test', surname='test')
        fixture_child_2 = Person(name='test2', surname='test2')
        fixture_parent = Person(name='test', surname='test',
                                first_child=fixture_child)

        self._repository.find_person = Mock(return_value=('test', fixture_parent))
        self._repository.get_person_id = Mock(return_value='test')
        self._repository.save_person = Mock()
        self._repository.update_person = Mock()

        self._sut.add_parent(fixture_child_2, fixture_parent)

        expected_child = deepcopy(fixture_child_2)
        expected_child.right_sibling = fixture_child

        expected_parent = deepcopy(fixture_parent)
        expected_parent.first_child = expected_child

        self._repository.update_person.assert_has_calls([call('test', expected_child),
                                                         call('test', expected_parent)])

    def test_add_non_stored_partner(self):
        fixture_person = Person(name='test', surname='test')
        fixture_partner = Person(name='test2', surname='test2')
        self._repository.find_person = Mock(return_value=None)
        self._sut.save_person = Mock()

        expected = deepcopy(fixture_person)
        expected.partner = fixture_partner
        self._sut.add_partner(fixture_person, fixture_partner)
        self._repository.save_person.assert_called_with(expected)

    def test_add_partner(self):
        fixture_person = Person(name='test', surname='test')
        fixture_partner = Person(name='test2', surname='test2')
        self._repository.find_person = Mock(return_value=('test', fixture_person))
        self._sut.save_person = Mock()

        expected = deepcopy(fixture_person)
        expected.partner = fixture_partner
        self._sut.add_partner(fixture_person, fixture_partner)
        self._repository.update_person.assert_called_with('test',
                                                          expected)
