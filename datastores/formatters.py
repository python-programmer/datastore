from typing import Any
import json

from datastores import messages


class BaseFormatter:

    def __init__(self) -> None:
        pass

    def load(self, source: str):
        raise NotImplementedError(messages.NOT_IMPLEMENTED_EXCEPTION)

    def dump(self, data: dict):
        raise NotImplementedError(messages.NOT_IMPLEMENTED_EXCEPTION)


class JsonFormatter(BaseFormatter):

    def load(self, source):
        return json.load(source)

    def dump(self, data: dict):
        return json.dumps(data)
