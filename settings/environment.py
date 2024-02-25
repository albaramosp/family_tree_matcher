
ENVIRONMENT = None


def set_environment(environment: str):
    global ENVIRONMENT
    ENVIRONMENT = environment


def get_environment() -> str | None:
    return ENVIRONMENT


class EnvironmentException(Exception):
    pass
