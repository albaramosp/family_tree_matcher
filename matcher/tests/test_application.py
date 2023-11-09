from unittest import TestCase
from unittest.mock import MagicMock

from matcher.application.use_cases import MatchSiblingsUseCase
from matcher.infrastructure.mongo_matcher import MongoMatcher
from person.infrastructure.mongo_repository import MongoPersonRepository
from person.public.exception import MalformedRequestException
from person.domain.model import Person


class MatchSiblingsUseCaseTestCase(TestCase):
    def setUp(self) -> None:
        self._repository = MagicMock(MongoPersonRepository)
        self.manager = MagicMock(MongoMatcher)
        self.sut = MatchSiblingsUseCase(manager=self.manager,
                                        repository=self._repository)

    def test_match_siblings_unregistered_person(self):
        with self.assertRaises(MalformedRequestException) as context:
            self.sut.execute(person=Person(
                name="test", surname="test"
            ))

        self.assertTrue('Person not found in the database'
                        in context.exception.__str__())

