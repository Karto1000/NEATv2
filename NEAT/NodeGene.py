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
from enum import Enum


class NodeType(Enum):
    INPUT = 0
    HIDDEN = 1
    OUTPUT = 2


class NodeGene:
    def __init__(self, x: float, y: float, *, node_type: NodeType):
        self.x: float = x
        self.y: float = y
        self.value: float = 0
        self.connections: list = []
        self.inno_num: int = None
        self.node_type = node_type

    def __eq__(self, other: 'NodeGene'):
        return self.inno_num == other.inno_num

    def __hash__(self):
        return self.inno_num

    def __repr__(self):
        return f"Gene<x: {self.x} y: {self.y}>"
