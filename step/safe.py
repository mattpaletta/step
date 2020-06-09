from typing import List

from step.step import Step


class SafeStep(Step):
    def __init__(self, levels = None, max_size = 100):
        super().__init__(levels, replicated = True, max_size = max_size)

    def set_batch(self, key: List[int], value: List[int], can_fail = False) -> List[int]:
        failed_keys = super(SafeStep, self).set_batch(key, value)
        if len(failed_keys) > 0 and can_fail:
            raise RuntimeError("Failed to insert {0} keys".format(len(failed_keys)))

        return failed_keys
