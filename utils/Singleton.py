from config.others import test
from config.product.sensexchange_business_config import sensexchange_business_path
from config.product.sensexperience_business_config import sensexperience_business_path
from config.product.sensexperience_platform_config import sensexperience_platform_path, \
    sensexperience_platform_ca_info
from config.server_info import server_info
from utils.mongodb import MongoDb


class ServerInfoConfig:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ServerInfoConfig, cls).__new__(cls)
            cls.instance.server_info = server_info
        return cls.instance


class SenseXchangeBusinessConfig:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SenseXchangeBusinessConfig, cls).__new__(cls)
            cls.instance.path = sensexchange_business_path
            database = MongoDb(test.get("mongo_uri"))
            db = database.connect_db(test.get("db"))
            cls.instance.db_config = db.sx_auto_test_config.find({"name": "sensexchange_business"})[0]
        return cls.instance


class SenseXperienceBusinessConfig:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SenseXperienceBusinessConfig, cls).__new__(cls)
            cls.instance.path = sensexperience_business_path
            database = MongoDb(test.get("mongo_uri"))
            db = database.connect_db(test.get("db"))
            cls.instance.db_config = db.sx_auto_test_config.find({"name": "sensexperience_business"})[0]
        return cls.instance


class SenseXperiencePlatformConfig:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SenseXperiencePlatformConfig, cls).__new__(cls)
            cls.instance.path = sensexperience_platform_path
            cls.instance.ca_info = sensexperience_platform_ca_info
            database = MongoDb(test.get("mongo_uri"))
            db = database.connect_db(test.get("db"))
            cls.instance.db_config = db.sx_auto_test_config.find({"name": "sensexperience_platform"})[0]
        return cls.instance

