from matcher.matcher import MongoMatcher, PersonAlreadyExists
from person.person import Person
import unittest
import json
import os
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

    def test_malformed_person(self):
        self.assertEqual([], self.sut.match(Person(None, None)))
        self.assertEqual([], self.sut.match(Person('alba', None)))

    def test_already_existing_person(self):
        fixture_person = Person('alba', 'ramos pedroviejo')
        self.assertRaises(PersonAlreadyExists, self.sut.match, fixture_person)

    def test_match(self):
        # Match one brother
        fixture_person = Person('julio', 'ramos pedroviejo')
        obtained = self.sut.match(fixture_person)
        self.assertEqual(len(obtained), 1)
        self.assertEqual(obtained[0]['name'], 'alba')
        self.assertEqual(obtained[0]['surname'], 'ramos pedroviejo')

        # Match several brothers

        # Match a parent

    def test_no_match(self):
        fixture_person = Person('julio', 'marquez dominguez')
        self.assertEqual(self.sut.match(fixture_person), [])



