from pymongo import MongoClient
from dotenv import load_dotenv
from os import getcwd, environ

load_dotenv(getcwd() + '/env_files/.env')

MONGO_DB_HOST = environ.get("MONGO_DB_HOST")
MONGO_DB_USER = environ.get("MONGO_DB_USER")
MONGO_DB_PASSWORD = environ.get("MONGO_DB_PASSWORD")

CLOUD_MONGO_CLIENT = MongoClient(MONGO_DB_HOST,
                                 username=MONGO_DB_USER,
                                 password=MONGO_DB_PASSWORD)
print(CLOUD_MONGO_CLIENT)
FAMILY_TREE_DATABASE = 'family_tree_matcher'
PEOPLE_COLLECTION = 'people'
