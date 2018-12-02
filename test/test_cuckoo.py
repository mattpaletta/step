from unittest import TestCase

from step.levels.cuckoo import Cuckoo
from step.step import Step


# Define some keys
cat = 1
dog = 2
mouse = 3


class TestStepCuckoo(TestCase):

    def test_set_single(self):
        data = Step(levels = [Cuckoo(n = 2)])
        data.set(key = cat, value = 1)
        x = data.get(key = cat)

        assert type(x) == int, "Dict returned incorrect type."
        assert x == 1, "Dict returned incorrect item."

    def test_get_empty(self):
        data = Step(levels = [Cuckoo(n = 2)])

        x = data.get(key = dog)
        assert x == -1, "Data returned incorrect value."

    def test_set_multiple(self):
        data = Step(levels = [Cuckoo(n = 2)])

        data.set(key = cat, value = 1)
        data.set(key = cat, value = 2)

        x = data.get(key = cat)
        assert x == 2, "Dictionary not updating values."

    def test_set_replace(self):
        # Assuming max_size = 2
        data = Step(levels = [Cuckoo(n = 2)])

        data.set(key = dog, value = 1)
        data.set(key = cat, value = 2)
        data.set(key = mouse, value = 3)

        data.set(key = dog + 3, value = 4)
        data.set(key = cat + 3, value = 5)
        data.set(key = mouse + 3, value = 6)

        x = data.get(dog)
        y = data.get(cat)
        z = data.get(mouse)
        assert z == 3, "Newest item not in dictionary"
        assert y == 2, "Second newest item not in dictionary"
        assert x == -1, "Oldest item not replaced"
