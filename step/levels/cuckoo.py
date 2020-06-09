from os import cpu_count
from typing import List, Union, Tuple, Type

import numpy as np
# from cuckoo.cpu.cuckoo import CuckooCpu

from step.level import Memory, GPU

class Cuckoo(Memory):
    # With auto_gpu we will automatically pick a GPU if available.
    def __init__(self, n: int, stash_size = 101, num_hash_functions = 4, num_parallel = cpu_count() - 1, auto_gpu = False):
        avail = False
        gpu = None
        if auto_gpu:
            avail, gpu = self._get_gpu()

        if avail and gpu is not None:
            self._cuckoo = gpu(n, stash_size, num_hash_functions, num_parallel)
        else:
            # self._cuckoo = CuckooCpu(n, stash_size, num_hash_functions, parallel = True)
            pass

    def set(self, key: List[int], value: List[np.uint64]) -> Tuple[List[Union[int, None]], List[int]]:
        did_enter = self._cuckoo.set(key, value)

        keys = []
        vals = []
        for i, v in zip(keys, value, did_enter):
            if not did_enter:
                keys.append(i)
                vals.append(v)
        return keys, vals

    def get(self, key: List[int]) -> List[Union[int, None]]:
        return self._cuckoo.get_multiple(key)

    def _get_gpu(self) -> Tuple[bool, Union[Type[GPU], None]]:
        # TODO: Add gpu version later (waiting on Cuckoo GPU implementation)

        # These are static so we don't have initialize until later.
        #cu = CUDA
        #cl = OpenCL

        # Return the one that is available, with if it's available.
        #if cu.is_available():
        #    return True, cu
        #elif cl.is_available():
        #    return True, cl
        #else:
        return False, None
