import random
import Filtro_Assembled as fa

class GenerationShip:
    """docstring for GenerationShip"""
    def __init__(self,family_number,circ_elements,gene_size,N_pop,verbose=True):
        super(GenerationShip, self).__init__()
        self.verbose=verbose
        self.family_number=family_number
        self.circ_elements=circ_elements
        self.gene_size=gene_size
        self.N_pop=N_pop
        self.generate_population()
        self.eval_fitness_pop()
        
    def generate_population(self):
        self.population=[]
        for n in range(self.N_pop):
            self.population.append(fa.Circus(self.circ_elements, self.gene_size))

        if self.verbose:
            for i in range(self.N_pop):
                print("{0} =>".format(i), end=' ')
                print(self.population[i].gene, end='\n')
    
    def eval_fitness_pop(self):
        self.fitness_pop=[]
        for circ in self.population:
            circ.add_jumpers()
            circ.assemble_circuit()
            self.fitness_pop.append(fa.eval_fitness(circ.circuit))

    def run_generations(self,generation_limit):
        best_fit=1e9
        #self.arq=open("family{}.dat".format(self.family_number),"w")
        for time in range(generation_limit):
            self.raise_generation()
            self.eval_fitness_pop()
            min_fit=min(self.fitness_pop)
            if min_fit<best_fit:
                ind=self.fitness_pop.index(min_fit)
                best_circuit=self.population[ind]
                print(best_circuit,min_fit)
                #self.arq.write(",".join(best_circuit))
                #self.arq.write(" {}\n".format(min_fit))
        #self.arq.write("bestão is: ")
        #self.arq.write(",".join(best_circuit))
        #self.arq.write(" {}\n".format(min_fit))
        #self.arq.close()

    def raise_generation(self):
        new_pop = []
        for i in range(int(self.N_pop/2)):
        #     parent1,parent2=self.selection()
            parent1,parent2=i,i*2
            child1,child2=fa.crossover(self.population[parent1],self.population[parent2],self.verbose)
            new_pop.append(child1)
            new_pop.append(child2)
        self.population=new_pop
        for c in range(0,self.N_pop,2):
            if self.verbose:
                print(self.population[c].gene)
            self.population[c].mutation()
            if self.verbose:
                print("mutante:" ,self.population[c].gene)

    def fight_club(self,fitness_pop,N_pop,n_fighters):
        fighters=random.sample(range(0,N_pop-1),n_fighters)
        if self.verbose:
            print('*1*',fighters)
        inc=1e99
        for j in range (n_fighters):
            if inc>fitness_pop[fighters[j]]:
                winner=fighters[j]
        return winner


    def selection(self):
        n_fighters=3
        pai=self.fight_club(self.fitness_pop, self.N_pop,n_fighters)
        fitness_without_father=self.fitness_pop[:pai]+self.fitness_pop[pai+1:]
        mae=self.fight_club(fitness_without_father,self.N_pop-1,n_fighters)
        if self.verbose:
            print(pai,mae)

        return  pai,mae


def create_family(family_number=0,number_of_generations=10 ):
    elementos = fa.elements
    N_pop = 6
    gene_size = 2
    family=GenerationShip(family_number,elementos,gene_size,N_pop,True)
    family.run_generations(number_of_generations)

if __name__ == "__main__":
    create_family(1,3)
    # n_gen=[10,20,30,40]
    # import multiprocessing as mp
    # pool = mp.Pool(processes=4)
    # results = [pool.apply_async(create_family, args=(fam,n_gen[fam])) for fam in range(4)]
    # output = [p.get() for p in results]

