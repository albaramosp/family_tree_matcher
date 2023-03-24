from matcher.matcher import MongoMatcher
import unittest
import json
import os
from settings import test
from mongomock import MongoClient


class TestMatcher(unittest.TestCase):
    def setUp(self):
        self.fixture_db = test.CLOUD_MONGO_CLIENT
        self.sut = MongoMatcher(test, self.fixture_db)

        with open(os.path.join(os.getcwd(), 'fixtures/fixture_documents.json'), 'r') as f:
            self.fixture_docs = json.loads(f.read())

        for pk in self.fixture_docs.keys():
            self.fixture_db[
                test.FAMILY_TREE_DATABASE][
                test.PEOPLE_COLLECTION].insert_one(self.fixture_docs[pk])

    def test_mocked_db(self):
        self.assertIsInstance(self.fixture_db, MongoClient)

    def test_match(self):
        self.sut.match({})
