from typing import List

from step.step import Step


class SafeStep(Step):
    def __init__(self, levels = None):
        super().__init__(levels, replicated = True)
        num_non_volatile = len(list(filter(lambda l: not l.is_volatile(), levels)))
        assert num_non_volatile > 0, "A safe step must have at least 1 non-volatile level."
    
    def set_batch(self, key: List[int], value: List[int], can_fail = False) -> List[int]:
        failed_keys = super(SafeStep, self).set_batch(key, value)
        if len(failed_keys) > 0 and can_fail:
            raise RuntimeError("Failed to insert {0} keys".format(len(failed_keys)))

        return failed_keys
