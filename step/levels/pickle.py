from typing import List, Union, Tuple

from step.level import Disk


class Pickle(Disk):
    def set(self, key: List[int], value: List[int]) -> Tuple[List[Union[int, None]], List[int]]:
        return super(Pickle, self).set(key, value)

    def get(self, key: List[int]) -> List[Union[int, None]]:
        return super(Pickle, self).get(key)
