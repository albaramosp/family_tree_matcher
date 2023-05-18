import unittest
import json
import os
from person.domain.driven.ports import NonExistingPerson
from matcher.infrastructure.mongo_matcher import MongoMatcher
from person.domain.model import Person
from settings import test
from mongomock import MongoClient


class TestMatcher(unittest.TestCase):
    fixture_db = test.CLOUD_MONGO_CLIENT

    @classmethod
    def setUpClass(cls):
        fixture_db = test.CLOUD_MONGO_CLIENT
        cls.sut = MongoMatcher(fixture_db)  # We can use the factory here

        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               'fixtures/fixture_documents.json'), 'r') as f:
            fixture_docs = json.loads(f.read())

        for pk in fixture_docs.keys():
            doc = fixture_docs[pk]
            doc['_id'] = pk
            fixture_db[
                test.FAMILY_TREE_DATABASE][
                test.PEOPLE_COLLECTION].insert_one(doc)

    def test_mocked_db(self):
        self.assertIsInstance(self.fixture_db, MongoClient)

    def test_match_siblings_unregistered_person(self):
        with self.assertRaises(NonExistingPerson) as context:
            self.sut.match_siblings(person=Person(
                name="test", surname="test"
            ))

        self.assertTrue('Person not found in the database'
                        in context.exception.__str__())

    def test_match_siblings_no_siblings(self):
        res = self.sut.match_siblings(person=Person(
            name="x", surname="x"
        ))
        self.assertEqual([], res)

    """
     z---->t---->y
    """
    def test_match_right_siblings(self):
        res = self.sut.match_siblings(person=Person(
            name="z", surname="z",
            right_sibling=Person(
                name="t", surname="t",
                right_sibling=Person(
                    name="y", surname="y"
                )
            )
        ))

        self.assertEqual(len(res), 2)
        self.assertTrue(Person(
                name="t", surname="t",
                right_sibling=Person(
                    name="y", surname="y"
                )
            ) in res)
        self.assertTrue(Person(
            name="y", surname="y"
        ) in res)

    def test_match_left_siblings(self):
        res = self.sut.match_siblings(person=Person(
            name="y", surname="y"
        )
        )

        self.assertEqual(len(res), 2)
        self.assertTrue(Person(
            name="t", surname="t",
            right_sibling=Person(
                name="y", surname="y"
            )
        ) in res)
        self.assertTrue(Person(
            name="z", surname="z",
            right_sibling=Person(name='t',
                                 surname='t',
                                 right_sibling=Person(
                                     name='y',
                                     surname='y'
                                 ))
        ) in res)

    def test_match_left_right_siblings(self):
        res = self.sut.match_siblings(person=Person(
            name="t", surname="t", right_sibling=Person(
                name="y", surname="y"
            )
        )
        )

        self.assertEqual(len(res), 2)
        self.assertTrue(Person(
            name='y',
            surname='y'
        ) in res)
        self.assertTrue(Person(
            name="z", surname="z",
            right_sibling=Person(name='t',
                                 surname='t',
                                 right_sibling=Person(
                                     name='y',
                                     surname='y'
                                 ))
        ) in res)
