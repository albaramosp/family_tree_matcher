from unittest import TestCase
from unittest.mock import MagicMock, Mock

from matcher.application.use_cases import MatcherUseCase
from matcher.infrastructure.mongo_matcher import MongoMatcher
from person.infrastructure.mongo_repository import MongoPersonRepository
from person.public.exception import MalformedRequestException
from person.domain.model import Person

from settings.test import CLOUD_MONGO_CLIENT


class MatchSiblingsUseCaseTestCase(TestCase):
    def setUp(self) -> None:
        self._repository = MongoPersonRepository(CLOUD_MONGO_CLIENT)
        self.manager = MagicMock(MongoMatcher)
        self.sut = MatcherUseCase(manager=self.manager,
                                  repository=self._repository)

    def test_match_siblings_unregistered_person(self):
        self._repository.get_person_id = Mock(return_value=None)
        with self.assertRaises(MalformedRequestException):
            self.sut.match_siblings(person=Person(
                name="test", surname="test"
            ))
