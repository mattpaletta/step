from typing import List, Union, Tuple

from step.level import GPU

try:
    from cuckoo.gpu import cuckoo_gpu
    _CUCKOO_CUDA = True
except ImportError:
    _CUCKOO_CUDA = False


class CUDA(GPU):
    def set(self, key: List[int], value: List[int]) -> Tuple[List[Union[int, None]], List[int]]:
        if _CUCKOO_CUDA:
            return super(CUDA, self).set(key, value)
        else:
            return super(CUDA, self).set(key, value)

    def get(self, key: List[int]) -> List[Union[int, None]]:
        if _CUCKOO_CUDA:
            return super(CUDA, self).get(key)
        else:
            return super(CUDA, self).get(key)

    @staticmethod
    def is_available() -> bool:
        return _CUCKOO_CUDA
