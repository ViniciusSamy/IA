from Envoriment import Enviroment
from copy import deepcopy

class AgentDFS:

    def __init__(self,env):
        self.env = env
    
    def act(self):
        #Initial percepts
        self.percepts = env.initial_percepts()

        #Definine frontier
        F = [ [self.percepts["initial_position"]] ]
        
        #Search Process
        finded = False
        while len(F) > 0:
            #Last element from frontier 
            print(f"F = {F}")
            current_path = F.pop()
            current_position = current_path[-1]
            
            print(current_position)

            #Send signal(position) and get perceptions(valid moves)
            action = { 'gived_position': current_position }
            self.percepts = env.signal(action)

            #Verifica se é a posição objetivo
            if self.percepts["reached_goal"]:
                print(f"Finded = {current_path}")

                finded = True
                return (finded, current_path)
                
            
            #Calculate available positions
            available_positions = []
            for move in self.percepts['available_moves']:
                available_positions.append([a + b for a, b in zip(move, current_position ) ])
            
            #Expand actual path
            for position in available_positions:
                new_path = deepcopy(current_path)
                
                if not (position in new_path):
                    new_path.append(position)
                    F.append(new_path)

        return (finded, None)
                
                





if __name__ == "__main__":
    #Create Enviroment
    height = 10
    width = 10
    n_obstacles = int ( (height*width) * 0.3 ) 
    env = Enviroment(height, width, n_obstacles)
    
    #
    agent = AgentDFS(env)
    finded, path = agent.act()

    #Printing Field
    if finded:
        import matplotlib.pyplot as plt
        from matplotlib.colors import ListedColormap
        cmap = ListedColormap(['w', 'r', 'b', 'g', 'y'])
        field_ = env.desing_path(path)
        print(field_)
        plt.matshow(field_ ,cmap=cmap)
        plt.show()


