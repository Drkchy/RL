import random


 
# RANDOM CHOICE FOR ACTION ====================================================

class RandomAgent(object):
    def __init__(self):
        self.choice = ['Left', 'Up', 'Down', 'Right']
        self.step = 0
        pass
        
    def act(self, game):
        self.step += 1
        print(self.step)
        return random.choice(self.choice)
    
    def reward(self, game, action):
        pass

# DEPTH LIMITED EXPECTIMAX - BASIC ============================================
        

class Basic_Expectimax_Agent(object):
    def __init__(self, depth = 2):
        self.choice = ['Left', 'Up', 'Down', 'Right']
        self.depth = depth
        self.step = 0
       
    def act(self, game):
        
        action, value = self.value(game, game.get_current_state(), 'max', self.depth)
        self.step += 1
        print(self.step)
        return action
        
    def value(self, game, state, next_agent, depth):
        
        if depth == 0 or len(game.get_actions(state))==0:

            max_cell = state[max(state)]
            free_tiles = 0.0
            sum_tiles = 0.0      
            
            for x_y in state:
                if not state[x_y]:
                    free_tiles += 1.0
                else:
                    sum_tiles += state[x_y]
                
            return (max_cell * 2) + (free_tiles * 1)  # retourn v = utility
        
        if len(game.get_actions(state))!=0:
        
            if next_agent == 'max': # MAX player turn
                estimation = [] #store estimations
                
                for action in game.get_actions(state):
                    
                    #Estimate successors_values and store them into tuples (action, values)
                    estimation.append((action, self.value(game, game.get_next_state(state, action),'exp', depth)[1]))
                
                return max(estimation, key=lambda item: item[1])
        
            
            else: # next_agent == 'exp': # RANDOM player = computer turn
    
                total = 0.0
                possible_states = game.get_possible_states(state) #S(t+1)
                
                if len(possible_states)!=0:
                    count_states = len(possible_states)
                else:
                    count_states = 1
                
                #Loop on collected possible successor states
                for possibility in possible_states:
                    if depth-1 == 0:
                        total += self.value(game, possibility, 'stop', depth-1 ) 
                    else:
                        total += self.value(game, possibility, 'max', depth-1 )[1] 
                return "", total/count_states
        

        
        #not in the presentation
        
class Depth_limited_Expectimax_Agent(object):
    def __init__(self, depth = 2):
        self.choice = ['Left', 'Up', 'Down', 'Right']
        self.depth = depth
        self.step = 0
       
    def act(self, game):
        action, value = self.value(game, game.get_current_state(), 'max', self.depth)
        self.step += 1
        print(self.step)
        return action


    def force_merge(self,state):
        count_merge = 0
        sum_merge = 0
        for x_y in state:
            if state[x_y]!=0:
                x, y = x_y
                if x > 0 and state[x-1, y]!=0:
                    if state[x_y] == state[x-1, y]:
                        count_merge  += 1
                        sum_merge += state[x_y] + state[x-1, y]

                elif y > 0 and state[x, y-1] !=0:
                    if state[x_y] == state[x, y-1]:
                        count_merge += 1
                        sum_merge += state[x_y] + state[x, y-1]

        return count_merge, sum_merge


    def force_edge(self, state):
        count_edge = 0
        sum_edge = 0
        for x_y in state:
            if state[x_y]!=0:
                if ((x_y[0] == 0) or (x_y[0] == 3)) and ((x_y[1] == 0) or (x_y[1] == 3)) :
                    count_edge +=1
                    sum_edge += state[x_y]
        return count_edge, sum_edge
    
    
    def is_edge(self, state, coordinates):
        is_edge = False
        if state[coordinates] != 0:
            if ((coordinates[0] == 0) or (coordinates[0] == 3)) and ((coordinates[1] == 0) or (coordinates[1] == 3)) :
                is_edge = True
        return is_edge
    

    def keep_free_tiles(self,state):
        count_free_tiles = 0
        for x_y in state:
            if state[x_y] == 0:
                count_free_tiles += 1
        return count_free_tiles
    
    
    def total_sum_grid(self, state):
        total_sum_grid = 0
        for x_y in state:
            total_sum_grid += state[x_y]
        return total_sum_grid
    
    
    def max_corner(self,state):
        count_snake = 0
        sum_snake = 0
        head_snake = max(state)
        if self.is_edge(state, head_snake) == True:
            count_snake =1
            sum_snake = state[head_snake]
        return count_snake, sum_snake


        
    def value(self, game, state, next_agent, depth):
        
        if depth == 0 or len(game.get_actions(state))==0:
            return self.force_merge(state)[1] + self.keep_free_tiles(state)  # retourn v = utility

        
        if next_agent == 'max': # MAX player turn
            estimation = [] #stock moyennes
            
            #max_branch = float('inf')
            #best_action = ""
            for action in game.get_actions(state):
                
                #Estimate successors_values and store them into tuples (action, values, )
                estimation.append((action, self.value(game, game.get_next_state(state, action),'exp', depth)[1]))
                #new_estimation = self.value(game, game.get_next_state(state, action),'exp', depth)[1]
                #if new_estimation > max_branch:
                #    best_action = action
                #    max_branch = new_estimation
            return max(estimation, key=lambda item: item[1])
            #return best_action, max_branch
        
        else: # next_agent == 'exp': # RANDOM player = computer turn

            total = 0.0
            possible_states = game.get_possible_states(state) #S(t+1)
            
            if len(possible_states)!=0:
                count_states = len(possible_states)
            else:
                count_states = 1
            
            #Loop on collected possible successor state
            for possibility in possible_states:
                if depth-1 == 0:
                    total += self.value(game, possibility, 'stop', depth-1 ) 
                else:
                    total += self.value(game, possibility, 'max', depth-1 )[1] 
            return "", total/count_states
        
        
# DEPTH LIMITED EXPECTIMAX - CUTOMIZED UTILITY FUNCTION =======================
        

class Customized_Expectimax_Agent(object):
    def __init__(self, depth = 2):
        self.choice = ['Left', 'Up', 'Down', 'Right']
        self.depth = depth
        self.step = 0
       
    def act(self, game):
        action, value = self.value(game, game.get_current_state(), 'max', self.depth)
        self.step += 1
        print(self.step)
        return action
        
    def value(self, game, state, next_agent, depth):
        
        if depth == 0 or len(game.get_actions(state))==0:

            #sum_total = self.total_sum_grid(state)
            count_free_tiles = self.keep_free_tiles(state) 
            #count_edge = self.force_edge(state)
            max_tile = state[max(state)]
            sum_weighted = self.sum_weighted(state)
            #count_snake = self.snake(state)
            
            return max_tile + count_free_tiles*7 + sum_weighted # retourn v = utility

        
        if next_agent == 'max': # MAX player turn
            estimation = [] 
            
            #if len(game.get_actions(state))==0:
            #    return random.choice(self.choice), 0
            
            for action in game.get_actions(state):
                
                #Estimate successors_values and store them into tuples (action, values, )
                estimation.append((action, self.value(game, game.get_next_state(state, action),'exp', depth)[1]))
            
            return max(estimation, key=lambda item: item[1])
    
        
        else: # next_agent == 'exp': # RANDOM player = computer turn

            total = 0.0
            possible_states = game.get_possible_states(state) #S(t+1)
            
            if len(possible_states)!=0:
                count_states = len(possible_states)
            else:
                count_states = 1
            
            #Loop on collected possible successor state
            for possibility in possible_states:
                if depth-1 == 0:
                    total += self.value(game, possibility, 'stop', depth-1 ) 
                else:
                    total += self.value(game, possibility, 'max', depth-1 )[1] 
            return "", total/count_states
        
             
        
    def force_edge(self, state):
        count_edge = 0
        for x_y in state:
            if state[x_y]!=0:
                if ((x_y[0] == 0) or (x_y[0] == 3)) and ((x_y[1] == 0) or (x_y[1] == 3)) :
                    count_edge +=1
        return count_edge
    
    def is_edge(self, state, coordinates):
        is_edge = False
        if state[coordinates] != 0:
            if ((coordinates[0] == 0) or (coordinates[0] == 3)) and ((coordinates[1] == 0) or (coordinates[1] == 3)) :
                is_edge = True
        return is_edge

    def keep_free_tiles(self,state):
        count_free_tiles = 0
        for x_y in state:
            if state[x_y] == 0:
                count_free_tiles += 1
        return count_free_tiles
    
    def total_sum_grid(self, state):
        total_sum_grid = 0
        for x_y in state:
            total_sum_grid += state[x_y]
        return total_sum_grid
    
    def sum_weighted(self,state):
        weights = {(0, 0): 0, (1, 0): 0, (2, 0): 0, (3, 0): 0,
                   (0, 1): 0, (1, 1): 0, (2, 1): 0, (3, 1): 0,
                   (0, 2): 0.25, (1, 2): 0.125, (2, 2): 0, (3, 2): 0,
                   (0, 3): 0.5, (1, 3): 1, (2, 3): 2, (3, 3): 4}
        total_weighted_grid = 0
        for cell_coord in state:
            total_weighted_grid += state[cell_coord]*weights[cell_coord]
        return total_weighted_grid
    
# =============================================================================
#     def snake(self, state):
#         count_snake = 0
#         head_snake = max(state)
#         keys = list(state.keys())
#         values = list(state.values())
#         if self.is_edge(state, head_snake) == True:
#             if all([keys[values.index(int(max(values)))] == (3,3),
#                keys[values.index(int(max(values)/2))] == (2,3),
#                keys[values.index(int(max(values)/(2*2)))] == (1,3),
#                keys[values.index(int(max(values)/(2*2*2)))] == (0,3),
#                keys[values.index(int(max(values)/(2*2*2*2)))] == (0,2),
#                keys[values.index(int(max(values)/(2*2*2*2*2)))] == (1,2),
#                keys[values.index(int(max(values)/(2*2*2*2*2*2)))] == (2,2)]):
#                    count_snake +=1
#             elif all([head_snake == (0,3),
#                keys[values.index(int(max(values)/2))] == (1,3),
#                keys[values.index(int(max(values)/(2*2)))] == (2,3),
#                keys[values.index(int(max(values)/(2*2*2)))] == (3,3),  
#                keys[values.index(int(max(values)/(2*2*2*2)))] == (3,2), 
#                keys[values.index(int(max(values)/(2*2*2*2*2)))] == (2,2), 
#                keys[values.index(int(max(values)/(2*2*2*2*2*2)))] == (1,2)]):
#                    count_snake +=1
#             elif all([head_snake == (0,0),
#                keys[values.index(int(max(values)/2))] == (1,0),
#                keys[values.index(int(max(values)/(2*2)))] == (2,0),
#                keys[values.index(int(max(values)/(2*2*2)))] == (3,0),  
#                keys[values.index(int(max(values)/(2*2*2*2)))] == (3,1),
#                keys[values.index(int(max(values)/(2*2*2*2*2)))] == (2,1), 
#                keys[values.index(int(max(values)/(2*2*2*2*2*2)))] == (3,1)]):
#                    count_snake +=1
#             elif all([head_snake == (3,0), 
#                keys[values.index(int(max(values)/2))] == (2,0),
#                keys[values.index(int(max(values)/(2*2)))] == (1,0), 
#                keys[values.index(int(max(values)/(2*2*2)))] == (0,0),  
#                keys[values.index(int(max(values)/(2*2*2*2)))] == (0,1), 
#                keys[values.index(int(max(values)/(2*2*2*2*2)))] == (1,1), 
#                keys[values.index(int(max(values)/(2*2*2*2*2*2)))] == (2,1)]):
#                    count_snake +=1
#         return count_snake
# =============================================================================
        
        
        
        
        
        
        
        
        
        
        
        