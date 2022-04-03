from typing import Any
from datastores.storages import BaseStorage

class Handler:

    def __init__(self, storage: BaseStorage) -> None:
        self.storage = storage

    def insert(self, key: Any, value: Any):
        source = self.storage.getData()
        source[key] = value
        self.storage.save(source)

    def bulk_insert(self, data: dict):
        source = self.storage.getData()
        source.update(data)
        self.storage.save(source)

    def get(self, key: Any):
        source = self.storage.getData()
        return source.get(key)

    def query(self, term: Any = None, limit: int = 10, offset: int = 0):
        source = self.storage.getData()
        result = []
        if term:
            for key, value in source.items():
                if value == term:
                    result.append({key: value})
        else:
            for key, value in source.items():
                result.append({key: value})
        
        return result[offset * limit: (offset * limit) + limit]

    def update(self, data: dict):
        source = self.storage.getData()
        source.update(data)
        self.storage.save(source)

    def delete(self, key: Any):
        source = self.storage.getData()
        source.pop(key)
        self.storage.save(source)