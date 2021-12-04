from QueensProblem import QueensProblem
from Neighborhood import neighborhood
from math import exp
from random import random
from copy import deepcopy

def SimulatedAnnealing(problem, neighborhood, T, T_min, cooling_factor, itr_max):

    #Current solution
    s = problem.random_solution()

    #Best solution finded
    s_star = deepcopy(s)

    #Search
    i = 0
    while T > T_min or i == itr_max:
       
        #Apply neighborhoods
        for N in neighborhood():

            #Apply neighborhood
            s_prime = N(s)

            #Calculate fitness
            f_s = problem.fitness(s)
            f_s_prime = problem.fitness(s_prime)
            f_s_star = problem.fitness(s_star)

            #Delta = variation of f(s) - f(s')
            delta = f_s - f_s_prime

           
            #Probability to accept
            try:
                prob = exp(-delta/T)
            
            #Prob too low
            except:
                prob = 0.0

      
            if delta>0:
                assert prob <= 1


            #Verify if f(s') > f(s)
            if delta < 0:
                s = deepcopy(s_prime)

                #Verify if is better than s*
                s_star = deepcopy(s_prime) if f_s_prime > f_s_star else s_star

            #Otherwise apply prob to accept
            elif  random() < prob:
                s = deepcopy(s_prime)

        
        #Cooling
        T = T - T*cooling_factor

        #Count itr
        i += 1
            

    #Return best solution finded
    return s_star


if __name__ == "__main__":
    
    #Set parameters
    num_queens = 10
    T = 100
    T_min = 0.000001
    cooling_factor = 0.01
    problem = QueensProblem(num_queens)
    neigh = neighborhood
    itr_max = 100

    s = SimulatedAnnealing(problem, neigh, T, T_min, cooling_factor, itr_max)



    problem.plot(s)
    
    



