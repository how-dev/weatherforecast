from typing import List, Optional, Dict, Type

from basic.basic_entity import BasicEntity
from basic.basic_persist_adapter import BasicPersistAdapter

import pymongo


class EntityNotFoundException(Exception):
    pass


class BasicMongoDBAdapter(BasicPersistAdapter):
    DATA_COLUMN_NAME = "data"

    def __init__(
        self,
        host: str,
        db_name: str,
        adapted_class: Type[BasicEntity],
        logger: Optional = None,
    ):
        super().__init__(adapted_class=adapted_class, logger=logger)
        self._client = pymongo.MongoClient(host)
        self._db = self._client[db_name]
        self._collection = self._db[self.adapted_class_name.lower()]

    def list_all(self):
        cursor = self._collection.find()

        items = []

        for db_item in cursor:
            json_data = db_item[self.DATA_COLUMN_NAME]

            item = self.adapted_class.from_json(json_data)
            item.set_adapter(self)

            items.append(item)

        return items

    def get_by_id(self, item_id, raise_exception=True):
        db_item = self._collection.find_one({"_id": item_id})

        if db_item:
            item = self.adapted_class.from_json(db_item[self.DATA_COLUMN_NAME])
            item.set_adapter(self)

            return item

        if raise_exception:
            raise EntityNotFoundException(
                f"Entity with id {item_id} not found"
            )

    def save(self, serialized_data: Dict):
        _id = serialized_data.get("entity_id")

        entity = self.get_by_id(_id, raise_exception=False)

        if entity:
            return self._collection.update_one(
                {"_id": _id},
                {"$set": {self.DATA_COLUMN_NAME: serialized_data}},
            ).upserted_id

        return self._collection.insert_one(
            {
                "_id": serialized_data["entity_id"],
                self.DATA_COLUMN_NAME: serialized_data,
            }
        ).inserted_id

    def delete(self, entity_id):
        self._collection.delete_one({"_id": entity_id})

        return entity_id

    def filter(self, *args, **kwargs):
        operators = self._get_operators(kwargs)
        cursor = self._collection.find(operators)

        items = []

        for db_item in cursor:
            json_data = db_item[self.DATA_COLUMN_NAME]
            item = self.adapted_class.from_json(json_data)
            item.set_adapter(self)

            items.append(item)

        return items

    def _get_operators(self, filters: Dict):
        keys = list(filters.keys())

        has_operator = any("__" in key for key in keys)

        if has_operator:
            operators = {}
            for key, value in filters.items():
                if "__" in key:
                    key, operator = key.split("__")
                    nested_key = f"{self.DATA_COLUMN_NAME}.{key}"
                    operators[nested_key] = {f"${operator}": value}
                else:
                    nested_key = f"{self.DATA_COLUMN_NAME}.{key}"
                    operators[nested_key] = {"$eq": value}
            return operators

        return {}
