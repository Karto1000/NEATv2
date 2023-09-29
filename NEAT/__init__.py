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

from NEAT.ConnectionGene import ConnectionGene
from NEAT.NodeGene import NodeGene, NodeType
from Species import Species
from utils import RandomHashSet


class NEAT:
    """
    This is the main class of the NEAT algorithm
    """

    def __init__(self, structure: tuple[int, int]):
        self.structure: tuple[int, int] = structure
        self.nodes: RandomHashSet[NodeGene] = RandomHashSet()
        self.connections: dict[ConnectionGene, ConnectionGene] = {}
        self.clients = []
        self.generation = 0

        self.__init_structure__()

    def __init_structure__(self):
        for i in range(self.structure[0]):
            node = NodeGene(0, i / 10, node_type=NodeType.INPUT)
            node.inno_num = i

            self.nodes.add(node, sort_key=lambda n: n.x)

        for i in range(self.structure[1]):
            node = NodeGene(1, i / 10, node_type=NodeType.OUTPUT)
            node.inno_num = i + self.structure[0]

            self.nodes.add(node, sort_key=lambda n: n.x)

    def get_new_node(self, x: float, y: float) -> NodeGene:
        node = NodeGene(node_type=NodeType.HIDDEN, x=x, y=y)
        node.inno_num = self.nodes.size() + 1
        self.nodes.add(node, sort_key=lambda n: n.x)

        return node

    def get_connection(self, from_node: NodeGene, to_node: NodeGene) -> ConnectionGene:
        connection = ConnectionGene(
            from_node=from_node,
            to_node=to_node
        )

        if existing_connection := self.connections.get(connection):
            connection.inno_num = existing_connection.inno_num
            return connection

        connection.inno_num = len(self.connections) + 1
        self.connections[connection] = connection
        return connection

    def get_nodes_with_x(self, x: float) -> list[NodeGene]:
        return list(filter(lambda n: n.x == x, self.nodes.list))

    def set_clients(self, clients: list):
        self.clients = clients

    def next_generation(self):
        # Selection
        species = []

        for client in self.clients:
            if len(species) == 0:
                species.append(Species(client))
                continue

            # Singular of species is also species lol
            for species_ in species:
                if species_.add(client):
                    # If the add operation was successful
                    break
            else:
                species.append(Species(client))

        new_species = []
        for species_ in species:
            species_.sort()
            species_.kill_half()

            # Remove species if only one client remains
            if len(species_.members) > 1:
                new_species.append(species_)

        # Crossover
        for client in self.clients:
            if client.species is None:
                species = random.choice(new_species)
                client.genome = species.breed()
