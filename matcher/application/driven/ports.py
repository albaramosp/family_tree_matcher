from abc import ABC, abstractmethod


class MatcherManager(ABC):
    @abstractmethod
    def match_siblings(self, person_id: str):
        ...

