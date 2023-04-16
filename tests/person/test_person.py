import unittest
from unittest.mock import patch

import mongomock
import pymongo

from person.person import MongoPersonRepository, IncorrectPerson, Person
from settings import test
import json
import os


class TestMongoPersonManager(unittest.TestCase):
    fixture_db = test.CLOUD_MONGO_CLIENT

    @classmethod
    def setUpClass(cls):
        cls.sut = MongoPersonRepository(cls.fixture_db)

        with open(os.path.join(os.getcwd(), 'fixtures/fixture_documents.json'), 'r') as f:
            fixture_docs = json.loads(f.read())

        for pk in fixture_docs.keys():
            doc = fixture_docs[pk]
            doc['_id'] = pk
            cls.fixture_db[
                test.FAMILY_TREE_DATABASE][
                test.PEOPLE_COLLECTION].insert_one(doc)

    def test_serialize(self):
        # Serialize incorrect person
        self.assertRaises(IncorrectPerson, self.sut.serialize, Person(None, None))
        self.assertRaises(IncorrectPerson, self.sut.serialize, Person('Alba', None))

        # Serialize simple person
        fixture = Person('Alba', 'Ramos Pedroviejo')
        obtained = self.sut.serialize(fixture)
        self.assertEqual({
            'name': 'Alba',
            'surname': 'Ramos Pedroviejo'
        }, obtained)

        # Serialize person with relatives
        fixture = Person('Alba',
                         'Ramos Pedroviejo',
                         partner=Person(
                             'Test',
                             'Test',
                             id='XXX'))
        obtained = self.sut.serialize(fixture)
        self.assertEqual({
            'name': 'Alba',
            'surname': 'Ramos Pedroviejo',
            'partner': 'XXX'
        }, obtained)

    @patch('mongomock.collection.Collection.insert_one')
    def test_save(self, mocked_insert_one):
        # A person who is already registered
        fixture = Person('alba',
                         'ramos pedroviejo')
        obtained = self.sut.save(fixture)
        self.assertEqual(obtained, '1')

        fixture = Person('david',
                         'demarco',
                         right_sibling=Person('laura', 'romero rodriguez'))
        obtained = self.sut.save(fixture)
        self.assertEqual(obtained, '7')

        # A person with the same name but different family, existing relative
        fixture_person = Person('alba',
                                'jimenez sanchez',
                                right_sibling=Person('lucas', 'jimenez sanchez'))

        self.sut.save(fixture_person)
        mocked_insert_one.assert_called_with({
            "name": 'alba',
            "surname": 'jimenez sanchez',
            "first_child": None,
            "right_sibling": '4',
            "partner": None
        })

        # A person with the same name but different family
        # Fake the sibling's inserted id
        mocked_insert_one.return_value = pymongo.results.InsertOneResult('mocked_id', 'mocked_id')
        fixture_person = Person('alba',
                                'ramos pedroviejo',
                                right_sibling=Person('sonia', 'ramos pedroviejo'))

        self.sut.save(fixture_person)
        mocked_insert_one.assert_called_with({
            "name": 'alba',
            "surname": 'ramos pedroviejo',
            "first_child": None,
            "right_sibling": 'mocked_id',
            "partner": None
        })

        # TODO insert a couple, how to handle the loop?
