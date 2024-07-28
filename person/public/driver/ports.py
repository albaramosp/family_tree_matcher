from abc import ABC, abstractmethod
from person.public.entities import AddParentRequestDto, PersonWithRelativesDto, AddPartnerRequestDto


class PersonManager(ABC):
    @abstractmethod
    def handle_save(self, rq: PersonWithRelativesDto):
        ...

    @abstractmethod
    def add_parent(self, rq: AddParentRequestDto):
        ...

    @abstractmethod
    def add_partner(self, rq: AddPartnerRequestDto):
        ...
