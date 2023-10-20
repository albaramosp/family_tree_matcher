from matcher.application.adapter import MatcherAdapter
from matcher.public.driver.ports import MatcherManager


def get_manager() -> MatcherManager:
    return MatcherAdapter()
