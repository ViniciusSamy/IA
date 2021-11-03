from random import shuffle, randint
from copy import deepcopy

def neighborhood():
    return [swap, advance_queen, retreat_queen]

def swap(solution):
    solution = deepcopy(solution)

    idxs = list(range(len(solution)))
    shuffle(idxs)
    i = idxs.pop()
    j = idxs.pop()

    solution[j], solution[i] = solution[i], solution[j]
    
    return solution

def advance_queen(solution):
    solution = deepcopy(solution)

    idx = randint(0, len(solution)-1)
    solution[idx] = (solution[idx] % len(solution)) +1

    return solution

def retreat_queen(solution):
    solution = deepcopy(solution)
    
    idx = randint(0, len(solution)-1)
    solution[idx] = ((solution[idx]-2) % len(solution) ) + 1


    return solution



if __name__ == "__main__":
    number_of_queens = 4
    sol =[ 1, 2, 3 ,4]

    #test random sol
    for i in range(1000):
        sol_ = swap(sol)
        print(sol_)
        assert len(sol_) == number_of_queens
        assert all( [ 1<=pos and pos <=10 for pos in sol_] )

        sol_ = advance_queen(sol)
        print(sol_)
        assert len(sol_) == number_of_queens
        assert all( [ 1<=pos and pos <=10 for pos in sol_] )

        sol_ = retreat_queen(sol)
        print(sol_)
        assert len(sol_) == number_of_queens
        assert all( [ 1<=pos and pos <=10 for pos in sol_] )







    