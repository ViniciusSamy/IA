from random import randint, shuffle, random
from QueensProblem import QueensProblem

def crossover(indv_1, indv_2):
    cut_1 = int(len(indv_1)/2)
    cut_2 = int(len(indv_2)/2)

    off_1 = indv_1[:cut_1] + indv_2[cut_2:]
    off_2 = indv_2[:cut_2] + indv_1[cut_1:]


    return off_1, off_2

def mutation(indv_1):
    idx = randint(0, len(indv_1)-1)
    
    valid_values = [ i+1 for i in range(len(indv_1)) if i+1 != indv_1[idx]]

    shuffle(valid_values)
    indv_1[idx] = valid_values.pop()

    return indv_1







def GeneticAlgorithm(problem, size_pop, num_generations, mutation_prob):
    pop = problem.random_population(size_pop)

    for _ in range(num_generations):


        #Tournament
        surviving_pop = []
        while pop:

            #If pop have inviduals enough to battle
            if len(pop) >= 2:
                
                #Select two indiviuals
                idx_1 = randint(0, len(pop)-1)
                indv_1 = pop.pop()
                f_1 = problem.fitness(indv_1)
                

                idx_2 = randint(0, len(pop)-1)
                indv_2 = pop.pop()
                f_2 = problem.fitness(indv_2)
                

                #Battle
                if f_1 >= f_2:
                    surviving_pop.append(indv_1)
                else:
                    surviving_pop.append(indv_2)

                

            #If haven't   
            else:
                indv = pop.pop()
                surviving_pop.append(indv)

            


        #Reprodution
        offspring_pop = []
        while len(surviving_pop) + len(offspring_pop) < size_pop:

            #Select two indiviuals
            all_indx = list(range(len(surviving_pop)))
            shuffle(all_indx)
            
            idx_1 = all_indx.pop()
            indv_1 = surviving_pop[idx_1]

            idx_2 = all_indx.pop()
            indv_2 = surviving_pop[idx_2]

            #Reproduce
            off_1, off_2 = crossover(indv_1, indv_2)

            #Guarantees the size of population
            if len(surviving_pop) + len(offspring_pop) + 2 <= size_pop:
                offspring_pop.append(off_1)
                offspring_pop.append(off_2)
            else:
                offspring_pop.append(off_1)


        
        #Merge Suviving and Offspring population
        pop = surviving_pop + offspring_pop

        #Mutation
        pop = [ indv if random() > mutation_prob else mutation(indv) for indv in pop  ]

    
    #Find Best Individual
    best = None
    f_best = float("inf") *-1
    for indv in pop:
        f_indv = problem.fitness(indv)

        if f_indv > f_best:
            best = indv
            f_best = f_indv
    
        
    #Return best individuals
    return best
        
        
    
            




if __name__ == "__main__":
    #Parameters
    num_queens = 10
    problem = QueensProblem(num_queens)
    size_pop = 100
    num_generations = 100
    prob_mutation = 0.1

    best = GeneticAlgorithm(problem, size_pop, num_generations, prob_mutation)

    problem.plot(best)
