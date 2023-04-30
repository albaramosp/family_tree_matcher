from abc import abstractmethod, ABC


class AbstractMatcher(ABC):
    @abstractmethod
    def match(self, person: dict) -> dict:
        """
        Match a person with its possibly related family

        :param person: dict of person
        :return dict of people who match
        """
        ...


