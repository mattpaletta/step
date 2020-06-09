from unittest import TestCase

from step.levels.pqdict import PQDict
from step.step import Step


# Define some keys
cat = 1
dog = 2
mouse = 3

class TestStepPQDict(TestCase):
    def _get_step(self):
        return Step(levels = [PQDict(max_size = 2)])

    def test_set_single(self):
        data = self._get_step()
        data.set(key = cat, value = 1)
        x = data.get(key = cat)

        assert type(x) == int, "Dict returned incorrect type."
        assert x == 1, "Dict returned incorrect item."

    def test_get_empty(self):
        data = self._get_step()

        x = data.get(key = dog)
        assert x is None, "Data returned incorrect value."

    def test_set_multiple(self):
        data = self._get_step()

        data.set(key = cat, value = 1)
        data.set(key = cat, value = 2)

        x = data.get(key = cat)
        assert x == 2, "Dictionary not updating values."

    def test_set_replace(self):
        # Assuming max_size = 2
        data = self._get_step()

        data.set(key = dog, value = 1)
        data.set(key = cat, value = 2)
        data.set(key = mouse, value = 3)

        x = data.get(dog)
        y = data.get(cat)
        z = data.get(mouse)
        assert z == 3, "Newest item not in dictionary"
        assert y == 2, "Second newest item not in dictionary"
        assert x is None, "Oldest item not replaced"
