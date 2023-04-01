import unittest
import json
import os

from matcher.matcher import MongoMatcher
from settings import test
from mongomock import MongoClient


class TestMatcher(unittest.TestCase):
    fixture_db = test.CLOUD_MONGO_CLIENT

    @classmethod
    def setUpClass(cls):
        cls.sut = MongoMatcher(cls.fixture_db)

        with open(os.path.join(os.getcwd(), 'fixtures/fixture_documents.json'), 'r') as f:
            fixture_docs = json.loads(f.read())

        for pk in fixture_docs.keys():
            cls.fixture_db[
                test.FAMILY_TREE_DATABASE][
                test.PEOPLE_COLLECTION].insert_one(fixture_docs[pk])

    def test_mocked_db(self):
        self.assertIsInstance(self.fixture_db, MongoClient)





