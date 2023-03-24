from interfaces.public import AbstractMatcher


class MongoMatcher(AbstractMatcher):
    def __init__(self, settings, database):
        self.settings = settings
        self.database = database

    def match(self, person: dict) -> dict:
        collection = self.database[
            self.settings.FAMILY_TREE_DATABASE][
            self.settings.PEOPLE_COLLECTION]
        print(collection.find_one({}))
        #print("AH")
        return {}
