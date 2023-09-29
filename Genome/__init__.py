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
from typing import Generator

from NEAT.ConnectionGene import ConnectionGene
from NEAT.NodeGene import NodeType, NodeGene
from utils import RandomHashSet, sigmoid


class Genome:
    """
    This class represents a single Genome, which is basically just a neural network
    """

    def __init__(self, neat, structure: tuple[int, int]):
        self.neat = neat
        self.structure = structure
        self.connections: RandomHashSet[ConnectionGene] = RandomHashSet()
        self.nodes: RandomHashSet[NodeGene] = RandomHashSet()

        self.__init_structure__()

    def __init_structure__(self):
        for i in range(self.structure[0]):
            input_node = NodeGene(0, i / 10, node_type=NodeType.INPUT)
            input_node.inno_num = i
            self.nodes.add(input_node, sort_key=lambda n: n.x)

        for i in range(self.structure[1]):
            output_node = NodeGene(1, i / 10, node_type=NodeType.OUTPUT)
            output_node.inno_num = self.structure[0] + i
            self.nodes.add(output_node, sort_key=lambda n: n.x)

    def add_node(self, connection: ConnectionGene) -> tuple[NodeGene, ConnectionGene, ConnectionGene]:
        if connection.split_to_node:
            new_node = connection.split_to_node
        else:
            new_node = self.neat.get_new_node(
                x=connection.to_node.x - (connection.to_node.x - connection.from_node.x) / 2,
                y=connection.to_node.y - (connection.to_node.y - connection.from_node.y) / 2
            )
            connection.split_to_node = new_node

        connection_from = self.neat.get_connection(
            from_node=connection.from_node,
            to_node=new_node
        )
        connection_from.weight = 1

        connection_to = self.neat.get_connection(
            from_node=new_node,
            to_node=connection.to_node
        )
        connection_to.weight = connection.weight
        connection_to.is_enabled = connection.is_enabled

        self.connections.remove_object(connection)
        self.connections.add(connection_from)
        self.connections.add(connection_to)
        self.nodes.add(new_node, sort_key=lambda n: n.x)

        return new_node, connection_from, connection_to

    def add_connection(self, from_node: NodeGene, to_node: NodeGene) -> ConnectionGene:
        connection = self.neat.get_connection(
            from_node=from_node,
            to_node=to_node
        )

        from_node.connections.append(connection)
        self.connections.add(connection)
        return connection

    @staticmethod
    def shift_weight(connection: ConnectionGene) -> float:
        connection.weight = max(-1, min(1, connection.weight + random.uniform(-1, 1)))
        return connection.weight

    @staticmethod
    def change_weight(connection: ConnectionGene) -> float:
        connection.weight = random.uniform(-1, 1)
        return connection.weight

    @staticmethod
    def toggle_connection(connection: ConnectionGene) -> bool:
        connection.is_enabled = not connection.is_enabled
        return connection.is_enabled

    def predict(self, inputs: list[float]) -> Generator[int, None, None]:
        if len(inputs) != self.structure[0]:
            raise Exception(f"Expected {self.structure[0]} inputs but got {len(inputs)}")

        for i, node in enumerate(self.nodes.list):
            if node.node_type == NodeType.INPUT:
                node.value = inputs[i]
            else:
                node.value = sigmoid(node.value)

            for connection in node.connections:
                if not connection.is_enabled:
                    continue

                connection.to_node.value = node.value * connection.weight

            if node.node_type == NodeType.OUTPUT:
                yield node.value

        for node in self.nodes.list:
            node.value = 0

    def distance(self, other: 'Genome') -> float:
        """
        Calculate the similarity of two genomes

        :param other: The genome to compare with
        :return: The similarity of the two genomes
        """

        self_sorted_connections = sorted(self.connections.list, key=lambda c: c.inno_num)
        other_sorted_connections = sorted(other.connections.list, key=lambda c: c.inno_num)

        if self_sorted_connections[-1].inno_num > other_sorted_connections[-1].inno_num:
            larger_connections = self_sorted_connections
            smaller_connections = other_sorted_connections
        else:
            larger_connections = other_sorted_connections
            smaller_connections = self_sorted_connections

        larger_index = 0
        smaller_index = 0

        disjoint_genes = 0
        weight_difference = 0
        similar_weights = 0

        while larger_index < len(larger_connections) and smaller_index < len(smaller_connections):
            larger_connection = larger_connections[larger_index]
            smaller_connection = smaller_connections[smaller_index]

            if larger_connection.inno_num == smaller_connection.inno_num:
                larger_index += 1
                smaller_index += 1
                similar_weights += 1
            elif larger_connection.inno_num > smaller_connection.inno_num:
                smaller_index += 1
                disjoint_genes += 1
            else:
                larger_index += 1
                disjoint_genes += 1

        weight_difference /= similar_weights if similar_weights > 0 else 1
        excess_genes = len(larger_connections) - larger_index

        n = max(len(larger_connections), len(smaller_connections))
        n = 1 if n < 20 else n

        return disjoint_genes / n + excess_genes / n + weight_difference

    def crossover(self, other: 'Genome') -> 'Genome':
        # TODO
        pass
