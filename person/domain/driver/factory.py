from person.domain.driver.ports import PersonManager
from person.domain.model import PersonOperationRequestDto, PersonOperationResponseDto, person_from_dto
from person.application.use_cases import SavePersonUseCase
from person.infrastructure.factory import create_mongo_person_repository


def get_manager() -> PersonManager:
    return DefaultManager()


class DefaultManager(PersonManager):
    """
    Manager that uses MongoDB for storage. Here, the factory method is used
    to create the repository and execute the use cases. Here, another factory
    method with another storage implementation could be used as long as it
    respects the abstraction agreement.
    """
    def handle_save(self, rq: PersonOperationRequestDto) -> PersonOperationResponseDto:
        person = person_from_dto(rq)
        res = PersonOperationResponseDto()
        try:
            SavePersonUseCase(repository=create_mongo_person_repository()).execute(person=person)
            res.person = rq
        except Exception as e:
            print("Exception: ", e)
            res.error = e
            res.error_code = 500

        return res
