from matcher.domain.driven.ports import MatcherManager
from person.domain.model import Person


class MatcherUseCase:
    def __init__(self, manager: MatcherManager):
        self.manager = manager


class MatchSiblingsUseCase(MatcherUseCase):
    def execute(self, person: Person):
        return self.manager.match_siblings(person)


class MatchHalfSiblingsUseCase(MatcherUseCase):
    def execute(self, person: Person):
        pass
