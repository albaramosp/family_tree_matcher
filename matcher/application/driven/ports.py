import abc
from abc import ABC


class MatcherManager(ABC):
    @abc.abstractmethod
    def match_siblings(self, person_id: str):
        ...

