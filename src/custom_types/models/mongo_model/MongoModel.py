from pydantic import BaseModel
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from abc import ABC, abstractmethod
# basemodel that has find, insert, update, delete methods
load_dotenv(override=True)
client = MongoClient(os.getenv("MONGO_URI"))
database = client[os.getenv("MONGO_DB")]
class MongoModel(BaseModel, ABC):
    @staticmethod
    @abstractmethod
    def collection() -> str:
        pass
    _id: str = ""
    @classmethod
    def find(cls, query):
        docs = database[cls.collection()].find(query)
        res = []
        for doc in docs:
            if not doc:
                continue
            res.append(cls.model_validate(doc))
        return res
    @classmethod
    def find_one(cls, query):
        doc = database[cls.collection()].find_one(query)
        if not doc:
            return None
        
        return cls.model_validate(doc)
    @classmethod
    def find_by_id(cls, id):
        doc = database[cls.collection()].find_one({"_id": id})
        if not doc:
            return None
        return cls.model_validate(doc)
    def save(self):
        data = self.model_dump()
        data.pop("_id", None)
        res = database[self.collection()].insert_one(data)
        self._id = res.inserted_id
    @classmethod
    def find_one_and_delete(self, query):
        database[self.collection()].find_one_and_delete(query)
    
    
    
    