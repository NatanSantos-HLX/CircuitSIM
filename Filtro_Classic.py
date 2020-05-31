import PySpice.Unit as PU
from PySpice.Spice.Netlist import Circuit
import numpy as np
import random


class Circus:

    def __init__(self, elements_list, N):
        self.elements_list = elements_list
        self.elements_names = list(elements_list.keys())
        self.quantity = N
        self.create_node_list()
        self.generate_gene()
        # self.draw_circuit()

    def create_node_list(self):
        self.node_list = ["Vin"]
        for i in range(0, self.quantity):
            n_node_list = ["n{}".format(i)][0]
            self.node_list.append(n_node_list)
        self.node_list.append("GND")

    def generate_gene(self):
        self.components = random.choices(self.elements_names, k=self.quantity)
        self.nodes = []
        for comp in self.components:
            start = np.random.randint(1, self.quantity)
            end = np.random.randint(start + 1, self.quantity + 1)
            self.nodes.append(self.node_list[start])
            self.nodes.append(self.node_list[end])
        self.check_out()
        self.assemble_gene()

    def check_out(self):
        self.out = random.choice(self.nodes)
        while (self.out == 'Vin') or (self.out == 'GND'):
            self.out = random.choice(self.nodes)

    def assemble_gene(self):
        self.gene = []
        for c, comp in enumerate(self.components):
            self.gene.append(self.nodes[2 * c])
            self.gene.append(comp)
            self.gene.append(self.nodes[2 * c + 1])
        self.gene.append(self.out)

    def mutation(self):
        for c in range(self.quantity):
            aux = random.randint(0, 100)
            if aux <= 5:
                self.components[c] = random.choice(self.elements_names)
        for n in range(self.quantity * 2):
            aux = random.randint(0, 100)
            if aux <= 5:
                self.nodes[n] = random.choice(self.node_list)
        self.assemble_gene()


def simple_cross(circ1, circ2, verbose=False):
    N = circ1.quantity
    cut = random.randint(0, len(circ1.gene))
    cross1 = circ1.gene[:cut] + circ2.gene[cut:]
    cross2 = circ2.gene[:cut] + circ1.gene[cut:]

    if verbose:
        print(circ1.gene, circ2.gene)
        print(cut)
        print(cross1, cross2)

    return cross1, cross2


def double_cross(circ1, circ2, verbose=False):
    N = circ1.quantity
    cut1 = random.randint(0, len(circ1.gene) - 2)
    cut2 = random.randint(cut1 + 1, len(circ1.gene))

    cross1 = circ1.gene[:cut1] + circ2.gene[cut1:cut2] + circ1.gene[cut2:]
    cross2 = circ2.gene[:cut1] + circ1.gene[cut1:cut2] + circ2.gene[cut2:]

    if verbose:
        print(circ1.gene, circ2.gene)
        print(cut1, cut2)
        print(cross1, cross2)

    return cross1, cross2


def crossover(circ1, circ2, verbose):
    chance = np.random.randint(0, 100)
    if chance < 30:
        cross1, cross2 = simple_cross(circ1, circ2, verb)
    elif chance >= 30:
        cross1, cross2 = double_cross(circ1, circ2, verb)
    return cross1, cross2


def assemble_circuit(circ, verbose=False):
    circ1.circuit_gene = circ1.gene
    begin = '0'
    if "Vin" not in circ.nodes:
        without_0 = True
        n = 0
        while without_0 == True:
            if "n{}".format(n) in circ1.nodes:
                begin = n
                without_0 = False
            else:
                n += 1
        circ1.circuit_gene = ["Vin" if x == "n{}".format(
            begin) else x for x in circ1.circuit_gene]
        if verbose:
            print("after first node correction:")
            print(circ1.circuit_gene)
    if "GND" not in circ.nodes:
        without_0 = True
        n = circ1.quantity - 1
        while without_0 == True:
            if "n{}".format(n) in circ1.nodes:
                end = n
                without_0 = False
            else:
                n -= 1
        circ1.circuit_gene = ["GND" if x == "n{}".format(
            end) else x for x in circ1.circuit_gene]
        if verbose:
            print("after last node correction:")
            print(circ1.circuit_gene)

    for n in range(begin + 1, circ1.quantity):
        pos = n
        node = "n{}".format(pos)
        count = circ1.circuit_gene.count(node)
        while count == 1:
            node = "n{}".format(pos)
            if pos == begin + 1:
                circ1.circuit_gene = ["Vin" if x ==
                                      node else x for x in circ1.circuit_gene]
                count = 2
            else:
                change = "n{}".format(pos - 1)
                circ1.circuit_gene = [change if x ==
                                      node else x for x in circ1.circuit_gene]
                count = circ1.circuit_gene.count(change)
                pos -= 1
    if verbose:
        print("after reconnections:")
        print(circ1.circuit_gene)

        counter={}
        count = circ1.circuit_gene.count("Vin")
        counter["Vin"]=count
        for n in range(begin + 1, circ1.quantity):
            node = "n{}".format(n)
            count = circ1.circuit_gene.count(node)
            counter[node]=count
        count = circ1.circuit_gene.count("GND")
        counter["GND"]=count
        print("number of connections", counter)

if __name__ == "__main__":
    elements = {"R1": (1, 500@PU.u_Ω),
                "R2": (2, 10@PU.u_kΩ),
                "R3": (3, 1@PU.u_kΩ),
                "R4": (4, 20@PU.u_kΩ),
                "C1": (1, 1@PU.u_uF),
                "C2": (2, 5@PU.u_uF),
                "C3": (3, 7@PU.u_uF),
                "L1": (1, 1@PU.u_uH),
                "L2": (2, 10@PU.u_uH),
                "L3": (3, 15@PU.u_uH)
                }
    verb = True
    N = 20
    circ1 = Circus(elements, N)
    # circ2=Circus(elements,N)

    # cross1,cross2=crossover(circ1,circ2,verb)
    print("original gene")
    print(circ1.gene)
    # print(circ1.nodes)
    # circ1.mutation()
    # print(circ1.gene)
    assemble_circuit(circ1, verb)
