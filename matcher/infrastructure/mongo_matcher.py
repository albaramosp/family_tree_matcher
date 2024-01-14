from typing import List, Optional

from person.infrastructure.factory import DefaultPersonRepositoryFactory
from matcher.application.driven.ports import MatcherManager


class MongoMatcher(MatcherManager):
    def __init__(self, client):
        self.client = client
        self.database = self.client['family_tree_matcher']
        self.collection = self.database['people']
        self.person_repository = DefaultPersonRepositoryFactory().create_person_repository()

    def match_siblings(self, person_id: str) -> List[dict]:
        instance = self.collection.find_one({
            '_id': person_id
        })
        result = []
        self._sibling_search(person_id=instance.get('right_sibling'),
                             result=result,
                             search_type='right')
        self._sibling_search(person_id=instance.get('_id'),
                             result=result,
                             search_type='left')
        return result

    def _sibling_search(self,
                        person_id: dict,
                        result: list,
                        search_type: str = "right") -> Optional[List[dict]]:
        """
        Search for siblings. For right search type, search for
        every right sibling link until end of chain given the
        initial person to search from. For example, given y as t's
        right sibling, if z states t as its right sibling, y is its
        sibling too.
        For left search type, search for person pointing whose
        right sibling link points to the given person and get
        back on the chain. For example, given y, search for t
        as it's pointing to y as right sibling, then search
        for z as it's pointing to t as right sibling.
           x
          /
         z---->t----y----...

        :param person_id: person to search for siblings
        :param search_type: right or left search types
        :return list of right siblings
        """
        if person_id is None:
            return
        else:
            key = '_id' if search_type == 'right' else 'right_sibling'
            people = self.collection.find({
                key: person_id
            })

            if people:
                for person in people:
                    parsed_person = self.person_repository.person_from_mongo_instance(person)
                    result.append(parsed_person)
                    self._sibling_search(
                        person_id=person.get('right_sibling') if search_type == 'right' else person.get('_id'),
                        result=result,
                        search_type=search_type)

    # TODO an observer pattern to update people when a family member is created
