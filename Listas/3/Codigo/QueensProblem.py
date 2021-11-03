from random import randint
import matplotlib.pyplot as plt
import numpy as np

class QueensProblem():

    def __init__(self, num_queens):
        self.n = num_queens

    def random_solution(self):
        n = self.n
        solution = [ randint(1,n) for i in range(n) ]  
        return solution
    
    def random_population(self, n_indiv):
        return [ self.random_solution() for i in range(n_indiv) ]

    def fitness(self, solution):
        sol = list(solution)
        conflicts = 0

        for i in range(len(sol)):
            for j in range(len(sol)):
                if i == j:
                    continue
                
                if sol[i] == sol[j]:
                    conflicts += 1
                elif abs(sol[i] - sol[j]) == abs(i-j):
                    conflicts +=1
        
        return conflicts*-1

    def plot(self, solution):
        n = self.n
        mat = np.zeros((n,n))
        f = self.fitness(solution)

        for i in range(len(solution)):
            column = solution[i]             
            mat[i][column-1] = 1.0


        plt.matshow(mat)
        major_ticks = np.arange(0, n, 1)
        plt.gca().set_xticks(major_ticks)
        plt.gca().set_yticks(major_ticks)
        #---------------COPY-------------#
        #source: https://stackoverflow.com/questions/28885279/matplotlibs-matshow-not-aligned-with-grid
        plt.gca().set_xticks([x - 0.5 for x in plt.gca().get_xticks()][1:], minor='true')
        plt.gca().set_yticks([y - 0.5 for y in plt.gca().get_yticks()][1:], minor='true')
        plt.grid(which='minor')
        #--------------------------------#

        plt.text(-2, -1.5, f"Fitness = {f}")
        plt.show()




if __name__ == "__main__":
    number_of_queens = 10
    p = QueensProblem(number_of_queens)

    #test random sol
    for i in range(100):
        sol = p.random_solution()
        assert len(sol) == number_of_queens
        assert all( [ 1<=pos and pos <=10 for pos in sol] )
    
    #test initial pop
    for i in range(100):
        size = 100
        pop = p.random_population(size)
        assert len(pop) == size
        assert all( [ len(sol) == number_of_queens for sol in pop ] )
        assert all( [ all( [ 1<=pos and pos <=10 for pos in sol] ) for sol in pop ] )




