from typing import List, Union, Tuple, Dict
import pickle
import os
from step.level import Disk
from threading import Lock

class Pickle(Disk):
    def __init__(self, directory: str = os.path.join(os.curdir, "step", "data"), partitions: int = 10, not_exist_ok = True) -> None:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok = True)
        self._directory = directory
        self._num_partitions = partitions
        self._alert_on_error = not_exist_ok
        self._partition_lock = Lock()
        self._initalize_partitions(directory, partitions)
    
    def _get_partition_for_key(self, key: int) -> str:
        return self._get_partition_name(self._directory, hash(key) % self._num_partitions)

    def _get_partition_name(self, directory: str, partition_num: int) -> str:
        return str(hash(directory + str(partition_num)))

    def _initalize_partitions(self, directory: str, num_partitions: int) -> None:
        for i in range(num_partitions):
            with open(os.path.join(directory, self._get_partition_name(directory, i) + ".pkl"), "wb") as f:
                pickle.dump({}, f)
    
    def _read_partition(self, partition: str) -> Dict[int, Union[int, None]]:
        if not os.path.exists(os.path.join(self._directory, partition + ".pkl")) and self._alert_on_error:
            raise FileNotFoundError("Failed to find partition")
        elif not os.path.exists(os.path.join(self._directory, partition + ".pkl")):
            return {}
        else:
            with open(os.path.join(self._directory, partition + ".pkl"), "rb") as f:
                return pickle.load(f)
    
    def _read_partition_for_key(self, key: int) -> Dict[int, Union[int, None]]:
        return self._read_partition(self._get_partition_for_key(key))
    
    def _write_partition(self, partition, data) -> None:
        with open(os.path.join(self._directory, partition + ".pkl"), "wb") as f:
            pickle.dump(data, f)

    def _write_partition_for_key(self, key: int, data) -> None:
        self._write_partition(self._get_partition_for_key(key), data)

    def set(self, key: List[int], value: List[int]) -> Tuple[List[Union[int, None]], List[int]]:
        with self._partition_lock as pl:
            for k, v in zip(key, value):
                cur_partition = self._read_partition_for_key(k)
                cur_partition.update({k: v})
                self._write_partition_for_key(k, cur_partition)
        
        return ([], [])

    def get(self, key: List[int]) -> List[Union[int, None]]:
        def get_key(k: int) -> Union[int, None]:
            return self._read_partition_for_key(k).get(k)

        return list(map(get_key, key))
