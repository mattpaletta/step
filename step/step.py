from typing import Union, List, Dict, Tuple

from step.level import Level
#from step.levels.cuckoo import Cuckoo
from step.levels.pickle import Pickle
from step.levels.pqdict import PQDict


class Step(object):
    __slots__ = ["_levels", "_replicated"]

    def __init__(self, levels: List[Level] = None, replicated = False, max_size = 100):
        # Replicated is whether they should be a cache for each other, or a split

        if levels is None:
            first_2_3 = int(max_size * (2 / 3))
            last_1_3 = max_size - first_2_3

            #levels = [Cuckoo(n = first_2_3), PQDict(max_size = last_1_3), Pickle()]
            levels = [PQDict(max_size = last_1_3), Pickle()]

        assert len(levels) > 0, "Must have at least 1 level."

        # self._levels: Dict[str, Level] = {}
        self._levels = levels

        for level in levels:
            assert issubclass(level.__class__, Level), "Levels must be a subclass of step.Level"
            # self._levels.update({level.__name__.lower(), level})

        self._replicated = replicated

    def get(self, key: Union[int, List[int]]) -> Union[int, List[int]]:
        if type(key) == int:
            return self.get_single(key)
        elif type(key) == list:
            return self.get_batch(key)
        else:
            raise TypeError("Key must be type int or List[int]")

    def get_single(self, key: int) -> int:
        return self.get_batch([key])[0]

    def set(self, key: Union[int, List[int]], value: Union[int, List[int]]) -> Union[int, List[int]]:
        if type(key) == int:
            return self.set_single(key, value)
        elif type(key) == list:
            return self.set_batch(key, value)
        else:
            raise TypeError("Key must be type int or List[int]")

    def set_single(self, key: int, value: int) -> List[int]:
        return self.set_batch([key], [value])

    def get_batch(self, key: List[int]) -> List[Union[int, None]]:
        output_array: List[int] = [None] * len(key)

        for level in self._levels:
            missing_indexes, missing_keys = self._indexes_missing(output_array, key)

            level_get_batch = level.get(missing_keys)

            # Put in the new value if it was missing, otherwise, use the old value.
            output_array = [new_val if was_missing else old_val for (new_val, old_val, was_missing)
                            in zip(level_get_batch, output_array, missing_indexes)]

            if len(missing_indexes) == 0:
                return output_array

        # If we didn't have it, there could be some empty's
        return output_array

    def set_batch(self, key: List[int], value: List[int]) -> List[int]:
        # Initially try and insert everything.
        missing_keys = key
        missing_value = value

        for level in self._levels:
            # Only insert whatever we haven't already

            # We might get the old keys and values (if the level swaps).
            new_missing_keys, new_missing_values = level.set(missing_keys, missing_value)

            # If it's replicated, every key must go in every level!
            if not self._replicated:
                # Update keep the ones that were not inserted
                # missing_keys = [old for (new, old) in zip(level_get_batch, missing_keys) if (new is not None)]
                # missing_value = [old for (new, old) in zip(level_get_batch, missing_value) if (new is not None)]

                missing_keys = new_missing_keys
                missing_value = new_missing_values

                if len(missing_keys) == 0:
                    return missing_keys

        # These are the ones we failed to insert
        return missing_keys

    def _indexes_found(self, arr: List[Union[int, None]], keys: List[int]) -> Tuple[List[bool], List[int]]:
        indexes = []
        vals = []
        for i, v in enumerate(arr):
            if v is not None:
                vals.append(keys[i])
            indexes.append(v is not None)

        return indexes, vals

    def _indexes_missing(self, arr: List[Union[int, None]], keys: List[int]) -> Tuple[List[bool], List[int]]:
        indexes = []
        vals = []
        for i, v in enumerate(arr):
            if v is None or v == -1:
                vals.append(keys[i])
            indexes.append(v is None)

        return indexes, vals

    def _get_num_missing(self, arr: List[int]):
        # We define a None as a missing value.
        return len(list(filter(lambda x: x is None, arr)))
