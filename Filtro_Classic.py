import PySpice.Unit as PU
from PySpice.Spice.Netlist import Circuit
import numpy as np
import random


Rshunt= ("Rshunt", 1@PU.u_mΩ)

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
        self.out = random.choice(self.node_list)
        while (self.out == 'Vin') or (self.out == 'GND'):
            self.out = random.choice(self.node_list)
        self.components = random.choices(self.elements_names, k=self.quantity)
        self.nodes = []
        for comp in self.components:
            start = np.random.randint(1, self.quantity)
            end = np.random.randint(start + 1, self.quantity + 1)
            self.nodes.append(self.node_list[start])
            self.nodes.append(self.node_list[end])
        self.assemble_gene()

    def assemble_gene(self):
        self.gene = [self.out]
        for c, comp in enumerate(self.components):
            self.gene.append(self.nodes[2 * c])
            self.gene.append(comp)
            self.gene.append(self.nodes[2 * c + 1])

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


def assemble_circuit(circ,verbose):
    #short-circuits
    conns_circuit={}
    for i in range(N):
        node1=circ.circuit_gene[i*3+1]
        component=circ.circuit_gene[i*3+2]
        node2=circ.circuit_gene[i*3+3]
        node=[node1,node2]
        node.sort()
        if (node1+node2 in conns_circuit):
            conns_circuit[node1+node2].append(component)
        else:
            conns_circuit[node1+node2]=[component]
    for n in range(len(circ.node_list)-1):
        node1 = circ.node_list[n]
        node2 = circ.node_list[n+1]
        if node1+node2 not in conns_circuit:
            circ.circuit_gene.append(node1)
            circ.circuit_gene.append("jumper")
            circ.circuit_gene.append(node2)
    return circ

def draw(circ):
    N=circ.quantity
    conns={}
    for i in range(N):
        node1=circ.gene[i*3]
        component=circ.gene[i*3+1]
        node2=circ.gene[i*3+2]
        node=[node1,node2]
        node.sort()
        if (node1+node2 in conns):
            conns[node1+node2].append(component)
        else:
            conns[node1+node2]=[component]
    print(conns)


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
    N = 5
    circ1 = Circus(elements, N)
    # circ2=Circus(elements,N)
    circ1.circuit_gene = circ1.gene

    # cross1,cross2=crossover(circ1,circ2,verb)
    print("original gene")
    print(circ1.gene)
    # print(circ1.nodes)
    # circ1.mutation()
    # print(circ1.gene)
    circ1=assemble_circuit(circ1, verb)
    print(circ1.circuit_gene)
    draw(circ1)
