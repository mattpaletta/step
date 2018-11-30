from typing import List, Tuple, Union

from step.level import GPU

try:
    from cuckoo.gpu import cuckoo_cl
    _CUCKOO_CL = True
except ImportError:
    _CUCKOO_CL = False


class OpenCL(GPU):
    def set(self, key: List[int], value: List[int]) -> Tuple[List[Union[int, None]], List[int]]:
        if _CUCKOO_CL:
            return super(OpenCL, self).set(key, value)
        else:
            return super(OpenCL, self).set(key, value)

    def get(self, key: List[int]) -> List[Union[int, None]]:
        if _CUCKOO_CL:
            return super(OpenCL, self).get(key)
        else:
            return super(OpenCL, self).get(key)

    @staticmethod
    def is_available() -> bool:
        return _CUCKOO_CL
