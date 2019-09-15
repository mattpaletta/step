from unittest import TestCase

from step.levels.pickle import Pickle
from step.step import Step


# Define some keys
cat = 1
dog = 2
mouse = 3


class TestStepPickle(TestCase):
    def _get_step(self):
        return Step(levels = [Pickle(directory = "/tmp")])

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
