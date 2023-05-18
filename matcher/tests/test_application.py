from unittest import TestCase
from unittest.mock import MagicMock, Mock

from matcher.application.use_cases import MatchSiblingsUseCase
from matcher.infrastructure.mongo_matcher import MongoMatcher
from settings.test import CLOUD_MONGO_CLIENT
from person.domain.driven.ports import MalformedRequestException
from person.domain.model import Person


class MatchSiblingsUseCaseTestCase(TestCase):
    def setUp(self) -> None:
        self.manager = MagicMock(MongoMatcher(CLOUD_MONGO_CLIENT))
        self.sut = MatchSiblingsUseCase(manager=self.manager)

    def test_match_siblings_unregistered_person(self):
        with self.assertRaises(MalformedRequestException) as context:
            self.sut.execute(person=Person(
                name="test", surname="test"
            ))

        self.assertTrue('Person not found in the database'
                        in context.exception.__str__())

