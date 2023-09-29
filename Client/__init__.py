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
from __future__ import annotations

import random
import typing

from Genome import Genome
from NEAT import NodeGene, ConnectionGene

if typing.TYPE_CHECKING:
    from Species import Species


class Client:
    def __init__(self, neat, structure: tuple[int, int]):
        self.genome: Genome = Genome(neat, structure)
        self.species: Species = None
        self.fitness: float = 0

    def add_random_node(self) -> tuple[NodeGene, ConnectionGene, ConnectionGene]:
        if self.genome.connections.size() == 0:
            raise Exception("No connection to split")

        connection = random.choice(self.genome.connections.list)
        return self.genome.add_node(connection)

    def add_random_connection(self) -> ConnectionGene:
        from_node = random.choice(list(filter(lambda n: n.x < 1, self.genome.nodes.list)))
        greater_x = list(filter(lambda n: n.x > from_node.x, self.genome.nodes.list))

        if len(greater_x) == 0:
            raise Exception(f"No greater connection to connect to for x {from_node.x}")

        to_node = random.choice(greater_x)

        for conn in from_node.connections:
            if conn.to_node.inno_num == to_node.inno_num:
                raise Exception("Tried to connect two nodes that are already connected")

        return self.genome.add_connection(from_node=from_node, to_node=to_node)

    def shift_random_weight(self) -> ConnectionGene:
        if connection := self.genome.connections.get_random_element():
            self.genome.shift_weight(connection)
            return connection

        raise Exception("No connection to shift weight of")

    def replace_random_weight(self) -> ConnectionGene:
        if connection := self.genome.connections.get_random_element():
            self.genome.shift_weight(connection)
            return connection

        raise Exception("No connection to replace weight with")

    def toggle_random_connection(self) -> ConnectionGene:
        if connection := self.genome.connections.get_random_element():
            self.genome.toggle_connection(connection)
            return connection

        raise Exception("No connection to toggle enabled status")

    def __repr__(self):
        return f"Client<fitness: {self.fitness}>"
