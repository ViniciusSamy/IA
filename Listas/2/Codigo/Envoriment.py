
import numpy as np

class Enviroment:
    def __init__(self, height, width, n_obstacles):
        #Save dimensions of the field
        self.dimensions = (height, width)
        
        #Save numeber of obstacles
        self.n_obstacles = n_obstacles

        #Field as matrix ( Values : 0 = Free / 1 = Busy  )
        self.field = np.zeros(self.dimensions, dtype=int)

        #Random select position of obstacles, initial and final positions
        positions = np.random.choice( height*width, n_obstacles + 2, replace=False)

        #Set obstacles, inital and final position
        for i in range(len(positions)):
            index_count = positions[i]
            (m_i, m_j) = ( int(np.floor(index_count/width)), index_count%width )
            
            #Obstacles
            if i < (len(positions) - 2):  
                self.field[m_i, m_j] = 1
            #Initial Position
            elif i < (len(positions) - 1):
                self.field[m_i, m_j] = 2
                self.initial_position = [m_i, m_j]
            #Final Position
            else: 
                self.field[m_i, m_j] = 3
                self.final_position = [m_i, m_j]
            
            
        


    
    def initial_percepts(self):

        return  {
                    "initial_position": self.initial_position,
                    "reached_goal": False,
                    "available_moves": self.__calc_available_moves(self.initial_position)  
                }
        

    def signal(self, action):
        reached_goal = False
        agent_position = action['gived_position']
        available_moves = []

        #Reached the goal position
        if agent_position == self.final_position:
            reached_goal = True
        
        else:
            available_moves = self.__calc_available_moves(agent_position)
        
        #return percepts
        return  {
                    "reached_goal": reached_goal,
                    "available_moves": available_moves
                }
        



    def __calc_available_moves(self, position):
        available_moves = []
        moves = [ [1,0], [1,1], [0,1], [-1,1], [-1,0], [-1,-1], [0,-1], [1,-1] ]
        for move in moves:
            new_position = [ a + b for a, b in zip(position, move) ] 
            
            
            if  0 <= new_position[0] and new_position[0] < self.dimensions[0] and\
            0 <= new_position[1] and new_position[1] < self.dimensions[1] and\
            self.field[new_position[0], new_position[1]] != 1:
                
                available_moves.append(move)
            
        return available_moves


    def __check_validity(self, position):
        return 0 <= position[0] and position[0] < self.dimensions[0] and\
                0 <= position[1] and position[1] < self.dimensions[1] and\
                self.field[position[0], position[1]] != 1

    def desing_path(self, path):
        field_ = self.field.copy()
        for [i, j] in path:
            print("in", i, j)
            if field_[i][j] == 0 :
                
                field_[i][j] = 4
        return field_
            






if __name__ == "__main__":
    
    #Create Enviroment
    height = 10
    width = 10
    n_obstacles = int ( (height*width) * 0.3 ) 
    env = Enviroment(height, width, n_obstacles)


    #Print inicial position and valid moves
    print(env.initial_percepts()['initial_position'])
    print(env.initial_percepts()['available_moves'])

    #Printing Field
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    cmap = ListedColormap(['w', 'r', 'b', 'g'])
    plt.matshow(env.field ,cmap=cmap)
    plt.show()

