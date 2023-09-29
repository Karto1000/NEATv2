# -----------------------------------------------------------
# Copyright (c) YPSOMED AG, Burgdorf / Switzerland
# YDS INNOVATION - Digital Innovation
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# email diginno@ypsomed.com
# author: Tim Leuenberger (Tim.leuenberger@ypsomed.com)
# -----------------------------------------------------------
import random
import typing
import math

T = typing.TypeVar("T")


class RandomHashSet(typing.Generic[T]):
    """
    This RandomHashSet class is used for efficient data retrieval and checking if the data is
    contained within the list
    """

    def __init__(self):
        self.list: list[T] = []
        self.set: set[T] = set()

    def contains(self, data: T) -> bool:
        return data in self.set

    def size(self) -> int:
        return len(self.list)

    def add(self, data: T, *, sort_key: typing.Callable[[T], int] = None):
        if data in self.set:
            return

        self.list.append(data)
        self.set.add(data)

        if sort_key:
            self.list.sort(key=sort_key)

    def get_random_element(self) -> typing.Optional[T]:
        if len(self.set) <= 0:
            return None

        return random.choice(self.list)

    def get_at_index(self, index: int) -> typing.Optional[T]:
        if index < 0 or index > self.size():
            return None

        return self.list[index]

    def remove_index(self, index: int):
        if index < 0 or index > self.size():
            return

        self.set.remove(self.list[index])
        self.list.pop(index)

    def remove_object(self, data: T):
        self.set.remove(data)
        self.list.remove(data)


def sigmoid(x):
    return 1 / (1 + math.exp(-x))
