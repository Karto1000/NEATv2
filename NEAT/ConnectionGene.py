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

from Config import Config
from NEAT.NodeGene import NodeGene


class ConnectionGene:
    def __init__(self, from_node: NodeGene, to_node: NodeGene):
        self.from_node = from_node
        self.to_node = to_node
        self.inno_num = None
        self.weight = random.uniform(-1, 1)
        self.is_enabled = True
        self.split_to_node = None

    def __eq__(self, other: 'ConnectionGene'):
        return self.from_node.__eq__(other.from_node) and self.to_node.__eq__(other.to_node)

    def __hash__(self):
        return self.from_node.inno_num * Config.MAX_NUMBER_OF_NODES + self.to_node.inno_num

    def __repr__(self):
        return f"Connection<from_x: {self.from_node.x} from_y: {self.from_node.y} to_x: {self.to_node.x} to_y: {self.to_node.y}"
