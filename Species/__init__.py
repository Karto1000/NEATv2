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

from Config import Config

if typing.TYPE_CHECKING:
    from Genome import Genome
    from Client import Client


class Species:
    def __init__(self, first_member):
        self.members: list[Client] = [first_member]
        self.first_member: Client = first_member

    def add(self, client) -> bool:
        if self.first_member.genome.distance(client.genome) < Config.MIN_DISTANCE:
            client.species = self
            self.members.append(client)
            return True
        return False

    def sort(self):
        self.members.sort(key=lambda c: c.fitness)

    def kill_half(self):
        half_length = len(self.members) // 2

        for client in self.members[:half_length]:
            client.species = None

        self.members = self.members[half_length:]

    def breed(self) -> Genome:
        first = random.choice(self.members)
        second = random.choice(list(filter(lambda c: c != first, self.members)))

        return first.genomde.crossover(second.genome)

    def __repr__(self):
        return f"Species<members: {self.members}>"
