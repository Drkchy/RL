import numpy as np

"""
Contains the definition of the agent that will run in an
environment.
"""



class RandomAgent:
    def __init__(self):
        """Init a new agent.
        """
    def act(self, observation):
        """Acts given an observation of the environment.
        Takes as argument an observation of the current state, and
        returns the chosen action.
        """
        return np.random.randint(0,9)
    def reward(self, observation, action, reward):
        """Receive a reward for performing given action on
        given observation.
        This is where your agent can learn.
        """
        pass


class Epsilongreedy:
    def __init__(self,nb_arms=10,epsilon=0.1):
        """Init a new agent"""
        self.epsilon=epsilon
        self.n=nb_arms
        self.Q_a=[np.random.rand()]*nb_arms
        self.N_a=np.ones(nb_arms)     
        self.counter=0
 
    def act(self,observation):
        """Acts given an observation of the environment.
        Takes as argument an observation of the current state, and
        returns the chosen action. """    
        random_nb=np.random.rand()
        #if self.counter<30 and self.epsilon==0:
        #    return np.random.randint(0,self.n)
        #elif random_nb>self.epsilon:
        if random_nb>self.epsilon:
            return np.argmax(self.Q_a)
        else: 
            return np.random.randint(0,self.n)

    def reward(self, observation, action, reward):
        """Receive a reward for performing given action on
        given observation. This is where your agent can learn.
        """    
        #reward = np.random.normal(0,1)  -> already set!!
        self.counter+=1
        self.N_a[action]+=1
        #updating average reward per action
        self.Q_a[action]=self.Q_a[action]*(self.N_a[action]-1)/self.N_a[action] + reward/self.N_a[action]

    
class OptimisticGreedy:
    
    #Obtained a final average reward of 1942.1411509
    def __init__(self,nb_arms=10,epsilon=0.01):
        """Init a new agent"""
        self.epsilon=epsilon
        self.n=nb_arms
        self.Q_a=[10+np.random.rand()]*nb_arms
        self.N_a=np.ones(nb_arms)     
        self.counter=0
 
    def act(self,observation):
        random_nb=np.random.rand()
        if random_nb>self.epsilon:
            return np.argmax(self.Q_a)
        else: 
            return np.random.randint(0,self.n)

    def reward(self, observation, action, reward):
        self.counter+=1
        self.N_a[action]+=1
        self.Q_a[action]=self.Q_a[action]*(self.N_a[action]-1)/self.N_a[action] + reward/self.N_a[action]


class SoftmaxAgent: 
    #Obtained a final average reward of 1654.77775777, tau=0.05
    #Obtained a final average reward of 1729.70839895, tau=0.1
    #Obtained a final average reward of 1851.78128678, tau=0.2
    #Obtained a final average reward of 1812.38004494, tau=0.3
    
    def __init__(self,nb_arms=10,tau=0.2):
        """Init a new agent"""
        self.tau=tau
        self.n=nb_arms
        self.N_a=np.zeros(nb_arms)
        self.Q_a=np.ones(nb_arms)

    def act(self, observation):
        """Compute softmax values """
        r=np.random.random()
        p_cml=0.0
        S = sum([np.exp(k/self.tau) for k in self.Q_a])
        proba = [np.exp(k/self.tau)/S for k in self.Q_a]
        pl= len(proba)
        
        for i in range(pl):
            proba_i = proba[i]
            p_cml += proba_i
            if p_cml>r:
                return i
    
    def reward(self, observation, action, reward):
        self.N_a[action]+=1
        self.Q_a[action]=self.Q_a[action]*(self.N_a[action]-1)/self.N_a[action] + reward/self.N_a[action]


class UCB_Agent: 

    def __init__(self,nb_arms=10):
        self.n=nb_arms
        self.Q_a=[0]*nb_arms
        self.N_a=[0.0]*nb_arms


    def act(self, observation):
        #Initialising
        S = len(self.N_a)
        for i in range(S):
            if self.N_a[i]==0:
                return i
        
        B_t = [0.0 for k in range(S)]
        t= sum(self.N_a)
        for k in range(S):
            error= (2*np.log(t)/self.N_a[k])**0.5
            B_t[k] = self.Q_a[k]+ error 
        return np.argmax(B_t)

    def reward(self, observation, action, reward):
        self.N_a[action]+=1
        self.Q_a[action]=self.Q_a[action]*(self.N_a[action]-1)/self.N_a[action] + reward/self.N_a[action]
    
    
# Choose which Agent is run for scoring
Agent = UCB_Agent


