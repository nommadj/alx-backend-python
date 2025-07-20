from typing import Mapping, Any, Sequence, Union
import requests


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    for key in path:
        nested_map = nested_map[key]
    return nested_map


def get_json(url: str) -> dict:
    response = requests.get(url)
    return response.json()


def memoize(method: Any) -> Any:
    attr_name = "_{}".format(method.__name__)

    def memoized(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)

    return memoized
