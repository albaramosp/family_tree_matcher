from matcher.application.driven.ports import MatcherManager
from matcher.infrastructure.mongo_matcher import MongoMatcher
from settings.pro import CLOUD_MONGO_CLIENT


def create_mongo_matcher_manager() -> MatcherManager:
    return MongoMatcher(client=CLOUD_MONGO_CLIENT)
