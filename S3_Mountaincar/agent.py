import numpy as np
from math import exp 

"""
Contains the definition of the agent that will run in an
environment.
"""

class RandomAgent:
    def __init__(self):
        """Init a new agent.
        """
    def reset(self, x_range):
        """Reset the state of the agent for the start of new game.
        Parameters of the environment do not change when starting a new 
        episode of the same game, but your initial location is randomized.
        x_range = [xmin, xmax] contains the range of possible values for x
        range for vx is always [-20, 20]
        """
        pass

    def act(self, observation):
        """Acts given an observation of the environment.
        Takes as argument an observation of the current state, and
        returns the chosen action.
        observation = (x, vx)
        """
        return np.random.choice([-1, 0, 1])

    def reward(self, observation, action, reward):
        """Receive a reward for performing given action on
        given observation. This is where your agent can learn.
        """
        pass

class TD_lambda_Agent:
    
    def __init__(self, gamma=0.9, lambda_=0.2, alpha=0.2):
        self.gamma = gamma
        self.lambda_ = lambda_
        self.alpha = alpha
        self.epsilon = 0.1
        self.Reward = 0
        self.delta = 0
        self.previous_state = None
        
        self.Q = {}

        self.k = 9
        self.p = 9
        
        self.actions = range(-1,2)
        
        self.dim = (self.k+1, self.p+1)
        self.W = {a:np.zeros((self.p + 1, self.k + 1)) for a in self.actions}
        self.e = np.zeros((len(self.actions),self.dim[0],self.dim[1]))
        self.S = np.zeros((self.k+1, self.p+1, 2)) 
        
        self.state = []
        for i in range(self.k+1):
            self.state.append([])
            for j in range(self.p+1):
                self.S[i][j]=(-150+float(i)*150/float(self.p),-20+float(j)*40/float(self.k))

    def reset(self,x_range):
        pass

    def getPhi(self, observation):
        
        # set the values of phi:
        for i in range(self.p+1):
            for j in range(self.k+1):
                phi = (np.exp(-(observation[0]-self.S[i][j][0])**2)/self.p)*(np.exp(-(observation[1]-self.S[i][j][1])**2)/self.k)     
        return phi      


    def act(self, observation):

        values = []
        # for a particular state and action, return the action that has the max value:
        if np.random.rand(1) < self.epsilon :
            return np.random.choice([-1, 0, 1])
        else:
            for i in range(3):
                values.append(self.Q.get((observation,i-2),0.0))
            return (values.index(max(values))-2)


    def reward(self, observation, action, reward):
        
        self.delta = self.Reward + self.gamma*self.W[action,:]*(self.getPhi(observation) - self.getPhi(self.previous_state))
        self.e = self.gamma*self.lambda_*self.e + self.getPhi(self.previous_state)
        self.w[action,:] = self.w[action,:] + self.alpha * self.delta * self.e 
        self.Q[(self.previous_state, self.action)] = np.sum(np.dot(self.W[action,:], self.phi)) 
        
        self.previous_state = observation
        self.action = action
        self.Reward = reward



class discrete_agent:
    def __init__(self):
        self.alpha=0.2
        self.gamma=0.9
        self.lambd=0.7
        self.epsilon=0.01
        
        self.a=0
        self.delta_t=0
        self.update=0

        self.count=0
        self.dmin=-150
        self.div=0 
        
        self.W=np.zeros((9,9,2))
        self.eligibility_grid=np.zeros((9,9,2))
        self.Wmax=np.random.choice([-1, 1])
        
        #initialise variables to update
        self.previous_state=(0,0)
        self.prv_action=np.random.choice([-1, 1])
        self.score=0
        
    def reset(self, x_range):
        
        self.count+=1
        self.dmin=x_range[0]
        self.div=int(float(self.dmin)/8)
        pass

    def act(self, observation):

        if np.random.random()<self.epsilon :
                return np.random.choice([-1, 1])
        else:
            x_int=int(observation[0]//self.div)
            vx_int=int((observation[1]+20)//5)
            
            self.Wmax=[self.W[x_int][vx_int][0],self.W[x_int][vx_int][1]]
            choix=self.Wmax.index(max(self.Wmax))
            if choix==0:
                return -1
            else:
                return 1

    def reward(self, observation, action, reward):

        self.eligibility_grid=np.dot(self.lambd*self.gamma,self.eligibility_grid)
        x_int=int(self.previous_state[0]//self.div)
        vx_int=int((self.previous_state[1]+20)//5)
        x_int_crr=int(observation[0]//self.div)
        vx_int_crr=int((observation[1]+20)//5)
        
        if action==-1:
            action=0
        
        self.eligibility_grid[x_int][vx_int][self.prv_action]+=1
        self.delta_t=self.alpha*(self.score+self.gamma*max(self.W[x_int_crr][vx_int_crr])-self.W[x_int][vx_int][self.prv_action])
        self.W=np.add(self.W,np.dot(self.delta_t,self.eligibility_grid))
        
        self.previous_state=observation
        self.prv_action=action
        self.score=reward
        
        pass

Agent = discrete_agent
