import os
from json.decoder import JSONDecodeError
from json import dumps
from typing import Any

import pytest
from datastores.handlers import Handler

from datastores.storages import LocalStorage
from datastores.formatters import JsonFormatter

# Since there are no primitive types in Python, I used this primitive types:
primitive = (int, str, bool, float)

class ValueObject:
    def __init__(self, id: int, value: Any) -> None:
        self.id = id
        self.value = value


@pytest.fixture()
def json_formatter():
    return JsonFormatter()


@pytest.fixture()
def local_storage_with_json_formatter(json_formatter):
    data_url = 'data_test.json'
    storage = LocalStorage(data_url, json_formatter)
    yield storage
    if os.path.exists(data_url):
        os.remove(data_url)


@pytest.fixture()
def handler(local_storage_with_json_formatter):
    return Handler(local_storage_with_json_formatter)


@pytest.fixture()
def new_data():
    return { 'key-1': 'value-1' }


@pytest.fixture()
def data_with_array_value():
    return { 'key-2': [1, 2, 3] }


@pytest.fixture()
def data_with_object_value():
    return { 'key-3': ValueObject(3, 'ok') }


@pytest.fixture()
def invalid_bulk_data():
    return { 'key-3': ValueObject(3, 'ok'), 'key-4': 88 }


@pytest.fixture()
def bulk_data():
    return { 'key-3': 'hadi', 'key-4': 88 }


@pytest.fixture()
def invalid_json_data():
    return 'A str value'


@pytest.fixture()
def invalid_json_file(invalid_json_data):
    data_url = 'test_data.json'
    with open(data_url, 'w') as stream:
        stream.write(invalid_json_data)
    
    with open(data_url, 'r') as stream:
        yield stream

    if os.path.exists(data_url):
        os.remove(data_url)


@pytest.fixture()
def valid_json_file(new_data):
    data_url = 'test_data.json'
    with open(data_url, 'w') as stream:
        stream.write(dumps(new_data))
    
    with open(data_url, 'r') as stream:
        yield stream
    
    if os.path.exists(data_url):
        os.remove(data_url)
    

# testing json formatter

def test_json_formatter_load_function_with_invalid_data(json_formatter, invalid_json_file):
    # Act, Assert
    with pytest.raises(JSONDecodeError):
        json_formatter.load(invalid_json_file)


def test_json_formatter_load_function_with_valid_data(json_formatter, valid_json_file, new_data):
    # Act
    result = json_formatter.load(valid_json_file)

    # Assert
    assert result == new_data
    

# testing local storage load and save functionalities

def test_get_data_from_local_storage_without_an_existing_file(local_storage_with_json_formatter: LocalStorage):
    # Act
    result = local_storage_with_json_formatter.getData()

    # Assert
    assert result == {}


def test_store_data_to_local_storage_and_get_data(local_storage_with_json_formatter: LocalStorage, new_data):
    # Act
    local_storage_with_json_formatter.save(new_data)
    data = local_storage_with_json_formatter.getData()

    # Assert
    assert data == new_data


def test_remove_a_file_storage_that_does_not_exists(local_storage_with_json_formatter: LocalStorage):
    # Act, Assert
    with pytest.raises(FileNotFoundError):
        local_storage_with_json_formatter.remove()


def test_remove_a_file_storage_that_exists(local_storage_with_json_formatter: LocalStorage, new_data):
    # Arrange
    # as soon as data is inserted into storage, the file storage for that is created
    local_storage_with_json_formatter.save(new_data)

    # Act
    assert local_storage_with_json_formatter.remove() == None


# testing handler functionalities

def test_insert_to_local_storage_with_json_formatter_with_invalid_data(handler: Handler, data_with_object_value: dict):
    # Act, Assert
    with pytest.raises(ValueError):
        data = list(data_with_object_value.items())[0]
        handler.insert(data[0], data[1])


def test_insert_to_local_storage_with_json_formatter_with_invalid_data_array(handler: Handler, data_with_array_value: dict):
    # Act, Assert
    with pytest.raises(ValueError):
        data = list(data_with_array_value.items())[0]
        handler.insert(data[0], data[1])


def test_insert_to_local_storage_with_json_formatter_with_invalid_data_array(handler: Handler, data_with_array_value: dict):
    # Act, Assert
    with pytest.raises(ValueError):
        data = list(data_with_array_value.items())[0]
        handler.insert(data[0], data[1])


def test_insert_to_local_storage_with_json_formatter_with_valid_data(handler: Handler, new_data: dict):
    # Act, Assert
    data = list(new_data.items())[0]
    assert handler.insert(data[0], data[1]) == None


def test_bulk_insert_to_local_storage_with_json_formatter_with_invalid_data(handler: Handler, invalid_bulk_data: dict):
    # Act, Assert
    with pytest.raises(ValueError):
        handler.bulk_insert(invalid_bulk_data)


def test_bulk_insert_to_local_storage_with_json_formatter_with_invalid_data(handler: Handler, bulk_data: dict):
    # Act
    handler.bulk_insert(bulk_data)
    result = handler.query()

    # Assert
    assert len(bulk_data) == len(result)