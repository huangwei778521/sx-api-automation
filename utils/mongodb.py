import re
from pymongo import MongoClient


class MongoDb:
    def __init__(self, mongo_uri):
        self.mongo_uri = mongo_uri
        self.client = None
        user_password = re.findall(re.compile(r'[//](.*?)[@]', re.S), self.mongo_uri)[0].split(":")
        self.user_name, self.password = user_password[0][1:], user_password[1]

    def connect_db(self, db_name):
        self.client = MongoClient(self.mongo_uri)
        db = self.client[db_name]
        return db

    def close_db(self):
        self.client.close()
