# datastore-y42 (development is in progress)
A datastore package that is used to store and retrieve arbitrary data in multiple formats &amp; destinations.


## Requirements
* [Python 3.7+](https://www.python.org/downloads/)


## Installation

### Project Requirements

Create a new virtualenv:

```
$ cd datastores-y42/
$ python3 -m venv venv
```

In the root directory of the project, run below command in the terminal:

```
pip install -r requirements.txt
```


## TODO List

* tests
* extend and test it with a custom yaml formatter
* extend and test it with a custom storage
* thread-safety
* I am busy, I haven't enough time 😅

## description

### Formatter
**Note**: everything (in this project) that we'd work with is, a Python dict. Thanks to Formatters that do this conversions for us

All formatters must inherit from the `datastores.storages.BaseFormatter` class:


```
class BaseFormatter:

    def __init__(self) -> None:
        pass

    def load(self, source: str):
        raise NotImplementedError(messages.NOT_IMPLEMENTED_EXCEPTION)

    def dump(self, data: dict):
        raise NotImplementedError(messages.NOT_IMPLEMENTED_EXCEPTION)
```

for example:

```
class JsonFormatter(BaseFormatter):

    def load(self, source):
        return json.load(source)

    def dump(self, data: dict):
        return json.dumps(data)
```

### Storage

**Question**: where to use the above formatter? **Storage**
All DataStores (storage) must inherit from the `datastores.storages.BaseStorage` class:


```
class BaseStorage:

    def __init__(self, url: str, formatter: BaseFormatter) -> None:
        self.url = url
        self.formatter = formatter

    def getData(self):
        raise NotImplementedError(messages.NOT_IMPLEMENTED_EXCEPTION)

    def save(self, data: str):
        raise NotImplementedError(messages.NOT_IMPLEMENTED_EXCEPTION)

    def remove(self, data: str):
        raise NotImplementedError(messages.NOT_IMPLEMENTED_EXCEPTION)
```

for example:

```
class   LocalStorage(BaseStorage):

    def __init__(self, url: str, formatter: BaseFormatter) -> None:
        # FIXME: url check, It is just for design and illustration
        super().__init__(url, formatter)

    def remove(self):
        os.remove(self.url)
    
    def getData(self):
        with open(self.url, 'r') as stream:
            # FIXME: performance issue, It is just for design and illustration
            return self.formatter.load(stream)

    def save(self, data: dict):
        with open(self.url, 'w') as stream:
            data = self.formatter.dump(data)
            stream.write(data)

    def remove(self):
        os.remove(self.url)
```

### handlers

**Question**: where to use the above storage? **Handler**

In handlers, We use the storage class to do all of our operations.

This is a first release of the Handler

This is just for design and demonstration, Obviously, This has performance issues

```
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
```

### How to use it

example:

```
from datastores.storages import LocalStorage
from datastores.formatters import JsonFormatter
from datastores.handlers import Handler

...

handler = Handler(LocalStorage('data.json', JsonFormatter()))

result = handler.query(offset=1, limit=5)
print(result)

handler.insert('key-77', 'yes')

handler.bulk_insert({'key-21': 'no', 'key-22': 'hello'})

handler.delete('key-77')
```