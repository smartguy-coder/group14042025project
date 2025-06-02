from abc import ABC, abstractmethod
from uuid import uuid4
from fastapi import HTTPException, status

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from schemas.product_schemas import ProductCreateSchema, ProductDataSchema, PatchProduct
from setting import settings


class BaseStorage(ABC):
    @abstractmethod
    def create_product(self, product: ProductCreateSchema):
        pass

    @abstractmethod
    def get_products(self):
        pass

    @abstractmethod
    def get_product(self, pk: str) -> ProductDataSchema:
        pass


class MongoStorage(ABC):
    def __init__(self):
        client = MongoClient(settings.MONGO_URI, server_api=ServerApi('1'))
        db = client[settings.DATABASE]
        collection = db[settings.COLLECTION]
        self.collection = collection

    def create_product(self, product: ProductCreateSchema) -> ProductDataSchema:
        payload = {
            'title': product.title,
            'description': product.description,
            'image': product.image,
            'price': product.price,

            'id': uuid4().hex,
        }
        self.collection.insert_one(payload)
        return payload

    def get_products(self, q: str = '') -> list[ProductDataSchema]:
        query = {}
        if q:
            query = {
                "$or": [
                    {'title': {'$regex': q, "$options": 'i'}},
                    {'description': {'$regex': q, "$options": 'i'}}
                ]
            }
        products = self.collection.find(query)
        return products

    def get_product(self, pk: str) -> ProductDataSchema | None:
        query = {'id': pk}
        product = self.collection.find_one(query)
        return product


    def delete_product(self, pk: str) -> None:
        query = {'id': pk}
        self.collection.delete_one(query)

    def patch_product(self, pk: str, product_data : PatchProduct) -> ProductDataSchema:
        query = {'id': pk}
        payload = {"$set": {"price": product_data.price, 'description': product_data.description} }
        updated = self.collection.update_one(query, payload)
        if updated.modified_count != 1:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
        return self.get_product(pk)



class FileStorage(ABC):
    def create_product(self, product: ProductCreateSchema):
        pass



storage = MongoStorage()
