from datastores.storages import LocalStorage
from datastores.formatters import JsonFormatter
from datastores.handlers import Handler


if __name__ == '__main__':
    handler = Handler(LocalStorage('data.json', JsonFormatter()))

    result = handler.query(offset=1, limit=5)
    print(result)

    handler.insert('key-77', 'yes')

    handler.bulk_insert({'key-21': 'no', 'key-22': 'hello'})

    handler.delete('key-77')
