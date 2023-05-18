from typing import List, Optional
from person.infrastructure.mongo_repository import MongoPersonRepository
from person.domain.model import Person
from person.domain.driven.ports import NonExistingPerson
from matcher.domain.driven.ports import MatcherManager


class MongoMatcher(MatcherManager):
    def __init__(self, client):
        self.client = client
        self.database = self.client['family_tree_matcher']
        self.collection = self.database['people']
        self.person_repository = MongoPersonRepository(client)

    def match_half_siblings(self, person: Person) -> List[Person]:
        #  x -- y       a -- y    y was married twice, secretly
        #   /            /        y had b with a and t&z with x
        #  /            /         y confesses b he has a lost brother, t
        # z-----t      b-----t    t doesn't know about b's existence
        #                         TODO half_sibling search should handle this case
        pass

    def match_siblings(self, person: Person) -> List[dict]:
        person_id = self.person_repository.get_person_id(person)

        if person_id:
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
        raise NonExistingPerson("Person not found in the database")

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
            person = self.collection.find_one({
                key: person_id
            })

            if person:
                parsed_person = self.person_repository.person_from_mongo_instance(person)
                result.append(parsed_person)
                self._sibling_search(person_id=person.get('right_sibling') if search_type == 'right' else person.get('_id'),
                                     result=result,
                                     search_type=search_type)

    # TODO an observer pattern to update people when a family member is created
