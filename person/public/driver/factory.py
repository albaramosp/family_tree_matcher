from person.public.driver.ports import PersonManager
from person.application.adapter import PersonAdapter


def get_manager() -> PersonManager:
    return PersonAdapter()
