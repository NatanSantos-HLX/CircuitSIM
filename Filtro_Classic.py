import PySpice.Unit as PU
from PySpice.Spice.Netlist import Circuit
import numpy as np
import random

class Circus:
    def __init__(self,elements_list,gene_size=0,gene=[]):
        self.elements_list=elements_list
        self.elements_names=elements_list.keys()
        if gene_size!=0:
            self.gene_size=gene_size
            self.generate_gene()
        if len(gene)!=0:
            self.gene=gene
            self.gene_size=len(gene)
        self.mutation()
        self.eval_fitness()
    
    def generate_gene(self):
        self.gene = random.sample(self.elements_names, k=self.gene_size)

    def add_component(self, component, position,name):
        if component[0] == "R":
            self.circuit.R(name, position[0],position[1],self.elements_list[component][1])
        elif component[0] == "C":
            self.circuit.C(name,position[0],position[1],self.elements_list[component][1])
        elif component[0] == "L":
            self.circuit.L(name, position[0],position[1],self.elements_list[component][1])

    def draw_circuit(self):
        positions = [('A', 'B'), ('B', 'out'), ('out', self.circuit.gnd)]
        for pos,component in enumerate(self.gene):
            self.add_component(component, positions[pos],pos)

    def mutation(self):
        for i in range(self.gene_size):
            aux = random.randint(0, 100)
            if aux <= 3:
                self.gene[i] = random.sample(self.elements_names, k=1)[0]

    
    def eval_fitness(self):
        self.circuit=Circuit('Low-Pass Filter')
        self.circuit.SinusoidalVoltageSource('input', 'A',  self.circuit.gnd, amplitude=1@PU.u_kV)
        # in case a shunt resistor is needed
        # circuit.R("shunt", 'master','A', 1@PU.u_Ω)
        # component_list = ["R1", "R2", "C1"]
        self.draw_circuit()
        simulator = self.circuit.simulator(temperature=25, nominnal_temperature=25)
        try:
            analysis = simulator.ac(start_frequency=150@PU.u_Hz, stop_frequency=3@PU.u_kHz, number_of_points=1, variation='dec')
            gain = 20 * np.log10(np.absolute(analysis.out)/(1@PU.u_V))
            delta_G = ((gain[1]) - (gain[0]))
            delta_F = (np.log10(3000) - np.log10(150))
            self.fitness = delta_G / delta_F
        except NameError:
            self.fitness=1e9

if __name__ == "__main__":
    elements={"R1": (1, 500@PU.u_Ω),
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
    gene_size=3
    circ1=Circus(elements, gene_size=gene_size)
    print(circ1.gene)
    print(circ1.fitness)
    gene=['R1','R2','C1']
    circ2=Circus(elements, gene=gene)
    print(circ2.gene)
    print(circ2.fitness)