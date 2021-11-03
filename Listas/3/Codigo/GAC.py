from itertools import product
from copy import deepcopy

def lt(X,Y):
    print(f"{X}<{Y} -> {X<Y}")
    return X<Y

def GAC(variables, constraints):

    new_variables = deepcopy(variables)

    to_do = [ (c['scope'][i], i, c) for c in constraints for i in range(len(c['scope'])) ]

    return GAC2(new_variables, constraints, to_do)
    

def GAC2(variables, constraints, to_do):
    
    while to_do:
        #Rescue current variable and constraint in to_do
        x, pos, c = to_do.pop(0)

        #Domain 
        D_x = variables[x]
        D_y = [ variables[y] for y in c['scope'] if y != x]
        

        #All combinations of D_y
        prod_D_y = list(product(*D_y))

        #Relation Constraint (Function Callback) 
        f = c['relation']


        #Valid Domain
        ND = [  x for x in D_x if any( [f( *(y[:pos] + (x, ) + y[pos:]) ) for y in prod_D_y] )  ]


        if ND != D_x:
            #Update to_do
            Z_C = [ (c['scope'][i], i ,c) for i in range(len(c['scope'])) if c['scope'] != x ]
            to_do += Z_C

            #Update domain of x 
            variables[x] = ND

    return variables





if __name__ == "__main__":
    variables = \
            {
                "A": [1, 2, 3, 4],
                "B": [1, 2, 3, 4],
                "C": [1, 2, 3, 4] 
            }


    constraints = \
            [
                { "scope": ["A", "B"], "relation": lambda X,Y: X<Y },
                { "scope": ["B", "C"], "relation": lambda X,Y: X<Y }
            ]

    new_var = GAC(variables, constraints)

    print(new_var)

    

    