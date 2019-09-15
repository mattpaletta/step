from abc import abstractmethod
from typing import List, Union, Tuple


class Level(object):
    @abstractmethod
    def is_volatile(self) -> bool:
        return True

    # If it's not implemented, it will fail to insert every item.
    def set(self, key: List[int], value: List[int]) -> Tuple[List[Union[int, None]], List[int]]:
        return key, value

    # If it's not implemented, fail to get every value.
    def get(self, key: List[int]) -> List[Union[int, None]]:
        return [None] * len(key)


class GPU(Level):
    def __init__(self, n: int, stash_size = 101, num_hash_functions = 4):
        pass

    def is_volatile(self) -> bool:
        return True

    @staticmethod
    def is_available() -> bool:
        return False


class Memory(Level):
    def is_volatile(self) -> bool:
        return True


class Disk(Level):
    def is_volatile(self) -> bool:
        return False
