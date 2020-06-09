# step

[![Build Status](https://travis-ci.com/mattpaletta/step.svg?branch=master)](https://travis-ci.com/mattpaletta/step)

## Instalation
To install Step:
```{bash}
pip install git+https://github.com/mattpaletta/step.git
```

## Getting Started
You can see examples in `test/`.

To create a new instance (with a maximum size of 10 elements):
```python
from step import Step
my_step = Step()
```

You can put elements in/out as follows:
```python
from step import Step
my_step = Step(max_size = 2) # max_size: (Optional) defaults to 100
my_step.set(key = "cat", value = 1) # Returns 1
my_step.get(key = "cat") # Returns 1
my_step.get(key = "dog") # Returns None
```

There are also wrapper functions available for getting/setting multiple items at  a time.
```python
from step import Step
my_step = Step(max_size = 100)
my_step.set(key = ["cat", "dog"], value = [1, 2])
my_step.get(key = ["cat", "dog", "mouse"]) # returns [1, 2, None]
```

### Making it safe
By default, Step will store all of the data in memory for maximum performance.  If you want to make it safe from crashes, you can do that in one of two ways.

The simpler version is to use the included `Safe` class.
```python
from step import SafeStep
my_step = SafeStep(max_size = 100) # max_size: (Optional) defaults to 100
my_step.set(key = "cat", value = 1) # Returns 1
my_step.get(key = "cat") # Returns 1
my_step.get(key = "dog") # Returns None
```
This code behaves exactly the same!  All it does under the hood is changes the default `steps` used to store data.  These steps are available to you if you want manual control.  Here is the equivalent example without `SafeStep`.
```python
from step import Step
from step.levels import Pickle
from step.levels import PQDict
my_step = Step(levels = [PQDict(max_size / (1/3)), Pickle()], replicated = True, max_size = 100) # max_size: (Optional) defaults to 100
my_step.set(key = "cat", value = 1) # Returns 1
my_step.get(key = "cat") # Returns 1
my_step.get(key = "dog") # Returns None
```
The decision was made that some of the levels are marked as volatile.  If `replicated = True`, which is default in `SafeStep`, then all of the data will be put in at least one non-volatile level, in addition to at least one volatile one.  `get` operations will try and read from the volatile storage first.  If volatile is `False`, data will be written to the first level, and only move into the second level when the first is full.

### Add New Levels
Adding a new backing-store is simple.  For example, suppose we want to store data in `MyDictObj`.  For simplicity, let's assume it has a `MyDictObj.set_item(key, value)` and `MyDictObj.get_item(key)` function.

```python
import step.level
class MyDict(level.Memory):
	def __init__(self, n: int):
		self._data = MyDictObj(max_size = n)

	def set(self, key: List[int], value: List[int]) -> Tuple[List[Union[int, None]]]:
		for k, v in zip(key, value):
			self._data.set_item(key = str(k), value = v)
		return key, value

	def get(self, key: List[int]) -> List[Union[int, None]]:
		output = []
		for k in key:
			output.append(self._data.get_item(key = str(k), default = None))
		return output
```
Because we inherited from `level.Memory`, Step uses this to determine this is a volatile step.   The other `level` types are:
* level.GPU
* level.Memory
* level.Disk

### Multiple Levels
Steps will be ordered (by default) in the order specified.  It is recommended to put the GPU, Memory, and Disk levels in this order as this will enable maximum performance.

In the event there are multiple volatile levels, data will always be written to the first, and moved to the next afterwards.

## Information

### Questions, Comments, Concerns, Queries, Qwibbles?

If you have any questions, comments, or concerns please leave them in the GitHub
Issues tracker:

https://github.com/mattpaletta/step/issues

### Bug reports

If you discover any bugs, feel free to create an issue on GitHub. Please add as much information as
possible to help us fixing the possible bug. We also encourage you to help even more by forking and
sending us a pull request.

https://github.com/mattpaletta/step/issues

## Maintainers

* Matthew Paletta (https://github.com/mattpaletta)

## License

GPL-3.0 License. Copyright 2020 Matthew Paletta. http://mrated.ca
