import unittest
from unittest.mock import Mock

from matcher.application.use_cases import MatcherUseCase
from person.application.driven.ports import PersonRepository
from matcher.infrastructure.mongo_matcher import MongoMatcher
from person.domain.model import Person


class TestMatcher(unittest.TestCase):
    def setUp(self):
        self._manager = Mock(MongoMatcher)
        self._person_repository = Mock(PersonRepository)
        self._sut = MatcherUseCase(self._manager, self._person_repository)

    def test_match(self):
        fixture = Person('test', 'test')
        self._person_repository.get_person_id.return_value = 'test'
        self._sut.match_siblings(fixture)
        self._manager.match_siblings.assert_called_once_with('test')
