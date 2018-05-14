import numpy as np


"""
Contains the definition of the agent that will run in an
environment.
"""

ACT_UP    = 1
ACT_DOWN  = 2
ACT_LEFT  = 3
ACT_RIGHT = 4
ACT_TORCH_UP    = 5
ACT_TORCH_DOWN  = 6
ACT_TORCH_LEFT  = 7
ACT_TORCH_RIGHT = 8

class RandomAgent:
    def __init__(self):
        """Init a new agent.
        """
    def reset(self):
        """Reset the internal state of the agent, for a new run.
        You need to reset the internal state of your agent here, as it
        will be started in a new instance of the environment.
        You must **not** reset the learned parameters.
        """
        pass

    def act(self, observation):
        """Acts given an observation of the environment.
        Takes as argument an observation of the current state, and
        returns the chosen action.
        Here, for the Wumpus world, observation = ((x,y), smell, breeze, charges)
        """
        return np.random.randint(1,9)

    def reward(self, observation, action, reward):
        """Receive a reward for performing given action on
        given observation.
        This is where your agent can learn.
        """
        pass


    
    # 150 explore, alph 0.05, 0.8

class Q_Learning_Agent:
      
    def __init__(self, gamma=0.99, alpha=0.7, epsilon=0.00005, counter=0):
        #(self, gamma=0.99, alpha=1, epsilon=0.001):
        #(self, gamma=0.9, alpha=0.9, epsilon=0.01):
        #(self, gamma=0.9, alpha=0.6, epsilon=0.001, counter=0):
        #(self, gamma=0.99, alpha=0.7, epsilon=0.00005, counter=0):
        self.epsilon=epsilon
        self.gamma=gamma
        self.alpha=alpha
        self.Q={}
        self.actions=range(1,5)
        self.t=10000
        self.counter=counter
        self.action_c=np.random.randint(1,5)
        self.current=()
        self.reward_c=0
    
    def reset(self):
        pass

    def getQ(self, observation, action):
        #return self.Q.get((observation, action), np.random.random())
        return self.Q.get((observation, action), 0.0)

    def act(self, observation):
        S=observation

        #add probability for exploration
        if np.random.random()<self.epsilon:
        #if np.random.random()<1/(self.t):
            if self.counter<900:
                action_t=np.random.randint(1,5)
                return action_t
        else:
            Q=[self.getQ(S,a) for a in self.actions]
            Q_max=max(Q)
            #in case we have two mamima for Qvalues 
            count=Q.count(Q_max)
            if count>1:
                bestaction=[i for i in range(len(self.actions)) if Q[i]==Q_max]
                i=np.random.choice(bestaction)
            else:
                i=Q.index(Q_max)
            
            action_t=self.actions[i]
            return action_t

    def reward(self, observation, action, reward):
        self.t+=1
        Q_new=max([self.getQ(observation,a) for a in self.actions])
        value=self.Q.get((self.current, self.action_c), None)
        if self.reward_c==-10 or self.reward_c==100:
                self.counter+=1
        if value is None:
            self.Q[(self.current, self.action_c)]=self.reward_c
        else:
            self.Q[(self.current, self.action_c)]=value+self.alpha*(self.reward_c+self.gamma*Q_new-value)
            
        self.current=observation
        self.action_c=action
        self.reward_c=reward
        #pass    

class Reflex_Q_Learning_Agent:
      
    def __init__(self, gamma=0.99, alpha=0.05, epsilon=0.0001, counter=0):
        self.epsilon=epsilon
        self.gamma=gamma
        self.alpha=alpha
        self.Q={}
        self.actions=range(1,5)
        self.t=10000
        self.counter=counter
        self.action_c=0
        self.current=()
        self.reward_c=0

    def reset(self):
        pass

    def getQ(self, observation, action):
        #return self.Q.get((observation, action), np.random.random())
        return self.Q.get((observation, action), np.random.random())

    def act(self, observation):
        S=observation

        if np.random.random()<self.epsilon:
        #if np.random.random()<1/(self.t):
            if self.counter<900:
                action_t=np.random.randint(1,9)
                return action_t
        else:
            Q=[self.getQ(S,a) for a in self.actions]
            Q_max=max(Q)
            #in case we have two mamima for Qvalues 
            count=Q.count(Q_max)
            if count>1:
                bestaction=[i for i in range(len(self.actions)) if Q[i]==Q_max]
                i=np.random.choice(bestaction)
            else:
                i=Q.index(Q_max)
            
            action_t=self.actions[i]
            return action_t

    def reward(self, observation, action, reward):
        self.t+=1
        Q_new=max([self.getQ(observation,a) for a in self.actions])
        value=self.Q.get((self.current, self.action_c), None)
        if self.reward_c==-10 or self.reward_c==100:
                self.counter+=1
        else:
            if self.current==observation:
                reward=reward*10
        if value is None:
            self.Q[(self.current, self.action_c)]=self.reward_c
        else:
            self.Q[(self.current, self.action_c)]=value+self.alpha*(self.reward_c+self.gamma*Q_new-value)
        self.current=observation
        self.action_c=action
        self.reward_c=reward
        #pass  

class Q_Learning_Agent_No_location:
    def __init__(self, gamma=0.99, alpha=0.65, epsilon=0.0001, counter=0):
        #(self, gamma=0.99, alpha=1, epsilon=0.001):
        #(self, gamma=0.9, alpha=0.9, epsilon=0.01):
        #(self, gamma=0.9, alpha=0.6, epsilon=0.001, counter=0):
        self.epsilon=epsilon
        self.gamma=gamma
        self.alpha=alpha
        self.Q={}
        self.actions=range(1,5)
        self.t=1000
        self.counter=counter
        self.action_c=0
        self.current=()
    
    def reset(self):
        pass

    def getQ(self, observation, action):
        #return self.Q.get((observation, action), np.random.random())
        return self.Q.get((observation, action), 0.0)

    def act(self, observation):
        S=observation[1:4]
        #self.current=S

        #add probability for exploration
        if np.random.random()<self.epsilon:
        #if np.random.random()<1/(self.t):
            if self.counter<900:
                action_t=np.random.randint(1,9)
                return action_t
        else:
            Q=[self.getQ(S,a) for a in self.actions]
            Q_max=max(Q)
            #in case we have two mamima for Qvalues 
            count=Q.count(Q_max)
            if count>1:
                bestaction=[i for i in range(len(self.actions)) if Q[i]==Q_max]
                i=np.random.choice(bestaction)
            else:
                i=Q.index(Q_max)
            
            action_t=self.actions[i]
            return action_t

    def reward(self, observation, action, reward):
        self.t+=1
        Q_new=max([self.getQ(observation[1:4],a) for a in self.actions])
        value=self.Q.get((self.current, self.action_c), None)
        if reward==-10 or reward==100:
                self.counter+=1
        if value is None:
            self.Q[(self.current, self.action_c)]=reward
        else:
            self.Q[(self.current, self.action_c)]=value+self.alpha*(reward+self.gamma*Q_new-value)
        self.current=observation[1:4]
        self.action_c=action
        #pass    
        
class Q_Learning_Agent_Past_Action:
    def __init__(self, gamma=0.9, alpha=0.2, epsilon=0.0001, counter=0):
        self.epsilon=epsilon
        self.gamma=gamma
        self.alpha=alpha
        self.Q={}
        self.actions=range(1,5)
        self.t=1000
        self.counter=counter
        self.action_c=0
        self.current=()
    
    def reset(self):
        pass

    def getQ(self, observation, action):
        #return self.Q.get((observation, action), np.random.random())
        return self.Q.get((observation, action), 0.0)

    def act(self, observation):
        S=observation[1:4]+(self.action_c,)
        #self.current=S

        #add probability for exploration
        if np.random.random()<self.epsilon:
        #if np.random.random()<1/(self.t):
            if self.counter<900:
                action_t=np.random.randint(1,9)
                return action_t
        else:
            Q=[self.getQ(S,a) for a in self.actions]
            Q_max=max(Q)
            #in case we have two mamima for Qvalues 
            count=Q.count(Q_max)
            if count>1:
                bestaction=[i for i in range(len(self.actions)) if Q[i]==Q_max]
                i=np.random.choice(bestaction)
            else:
                i=Q.index(Q_max)
            
            action_t=self.actions[i]
            return action_t

    def reward(self, observation, action, reward):
        self.t+=1
        Q_new=max([self.getQ(observation[1:4]+(self.action_c,),a) for a in self.actions])
        value=self.Q.get((self.current, self.action_c), None)
        if reward==-10 or reward==100:
                self.counter+=1
        if value is None:
            self.Q[(self.current, self.action_c)]=reward
        else:
            self.Q[(self.current, self.action_c)]=value+self.alpha*(reward+self.gamma*Q_new-value)
        self.current=observation[1:4]+(self.action_c,)
        self.action_c=action

Agent = Reflex_Q_Learning_Agent
