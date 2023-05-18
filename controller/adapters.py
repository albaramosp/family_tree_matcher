from typing import List

from person.domain.driver.factory import get_manager as get_person_manager
from person.domain.driver.ports import PersonManager
from person.domain.model import PersonOperationRequestDto, PersonOperationResponseDto

from matcher.domain.driver.factory import get_manager as get_matcher_manager
from matcher.domain.driver.ports import MatcherManager


class PersonAdapter(PersonManager):
    def handle_save(self, rq: PersonOperationRequestDto) -> PersonOperationResponseDto:
        return get_person_manager().handle_save(rq)


class MatcherAdapter(MatcherManager):
    def handle_match_siblings(self, rq: PersonOperationRequestDto) -> List[PersonOperationRequestDto]:
        return get_matcher_manager().handle_match_siblings(rq)
