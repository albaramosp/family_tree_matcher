from abc import abstractmethod, ABC
from typing import List
from person.domain.model import Person


class AbstractMatcher(ABC):
    @abstractmethod
    def match_siblings(self, person: Person) -> List[Person]:
        """
        Match a person with its possibly related siblings

        :param person: dict of person
        :return list of people who match
        """
        ...


