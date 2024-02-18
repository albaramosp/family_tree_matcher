import unittest

from mongomock import patch

from person.domain.model import Person
from person.infrastructure.mongo_repository import MongoPersonRepository
from settings import test
import json
import os


class TestMongoPersonRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        fixture_db = test.CLOUD_MONGO_CLIENT
        cls.sut = MongoPersonRepository(fixture_db)  # We can use the factory here

        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               'fixtures/fixture_documents.json'), 'r') as f:
            fixture_docs = json.loads(f.read())

        for pk in fixture_docs.keys():
            doc = fixture_docs[pk]
            doc['_id'] = pk
            fixture_db[
                test.FAMILY_TREE_DATABASE][
                test.PEOPLE_COLLECTION].insert_one(doc)

    @unittest.skip
    def test_save_existing(self):
        # A person who is already registered
        obtained = self.sut.save_person(Person('alba',
                         'ramos pedroviejo'))
        self.assertEqual(obtained, '1')

        fixture = Person('david',
                         'demarco',
                         right_sibling=Person('laura', 'romero rodriguez'))
        obtained = self.sut.save_person(fixture)
        self.assertEqual(obtained, '7')

    @unittest.skip
    @patch('mongomock.collection.Collection.insert_one')
    def test_save_with_existing_relative(self, mocked_insert_one):
        # A person with the same name but different family, existing relative
        fixture_person = Person('alba',
                                'jimenez sanchez',
                                right_sibling=Person('lucas', 'jimenez sanchez'))

        self.sut.save_person(fixture_person)
        mocked_insert_one.assert_called_with({
            "name": 'alba',
            "surname": 'jimenez sanchez',
            "first_child": None,
            "right_sibling": '4',
            "partner": None
        })

    @unittest.skip
    @patch('mongomock.collection.Collection.insert_one')
    def test_save_with_new_relative(self, mocked_insert_one):
        # A person with the same name but different family
        # Fake the sibling's inserted id
        mocked_insert_one.return_value = pymongo.results.InsertOneResult('mocked_id', 'mocked_id')
        fixture_person = Person('alba',
                                'ramos pedroviejo',
                                right_sibling=Person('sonia', 'ramos pedroviejo'))

        self.sut.save_person(fixture_person)
        mocked_insert_one.assert_called_with({
            "name": 'alba',
            "surname": 'ramos pedroviejo',
            "first_child": None,
            "right_sibling": 'mocked_id',
            "partner": None
        })

        # TODO insert a couple, how to handle the loop?"""