import os
from typing import Any

from datastores import messages
from datastores.formatters import BaseFormatter


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