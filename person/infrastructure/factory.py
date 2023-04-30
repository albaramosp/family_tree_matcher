from settings.pro import CLOUD_MONGO_CLIENT
from person.domain.driven.ports import PersonRepository
from person.infrastructure.mongo_repository import MongoPersonRepository


def create_mongo_person_repository() -> PersonRepository:
    """
    Creates a person repository from a given client. The repository's
    implementation can change here, but the interface will be
    respected, therefore application layer will not notice any
    changes in implementation as long as the interface is kept.
    """
    return MongoPersonRepository(client=CLOUD_MONGO_CLIENT)
