from unittest import TestCase
from unittest.mock import MagicMock, Mock

from matcher.application.use_cases import MatcherUseCase
from person.infrastructure.mongo_repository import MongoPersonRepository
from person.public.exception import MalformedRequestException
from person.domain.model import Person
from settings.environment import set_environment


class MatchSiblingsTestCase(TestCase):
    def setUp(self) -> None:
        set_environment("test")
        self._repository = MongoPersonRepository()
        self.sut = MatcherUseCase(repository=self._repository)

    def test_match_siblings_unregistered_person(self):
        self._repository.get_person_id = Mock(return_value=None)
        with self.assertRaises(MalformedRequestException):
            self.sut.match_siblings(person=Person(
                name="test", surname="test"
            ))
