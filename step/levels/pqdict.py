from typing import List, Union, Tuple

from step.level import Memory
from threadlru import LRUCache


class PQDict(Memory):
    def __init__(self, max_size: int):
        self._pq_dict = LRUCache(max_size)

    def set(self, key: List[int], value: List[int]) -> Tuple[List[Union[int, None]], List[int]]:
        for k, v in zip(key, value):
            # TODO:// Remove the old keys if not in the pqdict by function command.
            self._pq_dict.set(key = str(k), value = v)
        return key, value

    def get(self, key: List[int]) -> List[Union[int, None]]:
        output = []
        for k in key:
            output.append(self._pq_dict.get(key = str(k), default = None))
        return output
