import numpy as np

"""
Contains the definition of the agent that will run in an
environment.
"""

class ActorCriticPolicyGradientAgent:

	def __init__(self):
		self.average_reward = 0.0
		self.step = 0

		self.p = 20
		self.k = 20
		self.s = np.zeros((self.p+1,self.k+1,2))
		self.gamma = 0.95

		self.n = 0.4
		self.sigma = 20.0

		# Actor parameters: l = lambda, e = trace, a = alpha
		self.w = np.random.rand(self.p + 1, self.k + 1)
		self.e_w = np.zeros((self.p + 1, self.k + 1))
		self.l_w = 0.8
		self.a_w = 0.1

		# Critic parameters: l = lambda, e = trace, a = alpha
		self.theta = np.random.rand(self.p + 1, self.k + 1)
		self.e_theta = np.zeros((self.p + 1, self.k + 1))
		self.l_theta = 0.8
		self.a_theta = 0.1

		self.last_P = None
		self.last_state = None
		self.last_action = None
		self.last_reward = None
		self.game = 0

	def reset(self, x_range):

		# Reset average reward?
		self.average_reward = 0.0

		# Reset s
		for i in range(self.p + 1):
			for j in range(self.k + 1):
				self.s[i,j,0] = x_range[0] + float(i)*(x_range[1] - x_range[0])/float(self.p)
				self.s[i,j,1] = -10.0 + float(j)*40.0/float(self.k)

		# Reset the traces
		self.e_theta = np.zeros((self.p + 1, self.k + 1))
		self.e_w = np.zeros((self.p + 1, self.k + 1))

		self.last_action = None
		self.last_reward = None
		self.last_state = None
		self.last_P = None
		self.average_reward = 0.0
		self.step = 0
		self.game += 1


	def phi(self, i, j, x, vx):
		s_1 = self.s[i,j,0]
		s_2 = self.s[i,j,1]
		a = np.exp(-((x - s_1) ** 2) / self.p)
		b = np.exp(-((vx - s_2) ** 2) / self.k)
		return a * b

	# Returns a (p + 1) * (k + 1) matrix filled with phi values
	def Phi(self, obs):
		x, vx = obs
		val = np.zeros(((self.p+1), (self.k+1)))
		for i in range(self.p + 1):
			for j in range(self.k + 1):
				val[i,j] = self.phi(i, j, x, vx)
		return val

	def act(self, observation):
		self.step += 1

		P_ = self.Phi(observation)

		mu = sum(sum(self.theta*P_))
		self.sigma = 20.0 / np.log(self.step + 1)

		if self.game >= 180:
			return mu

		if self.last_action is not None:

			# Get phi for the current state and reshape it into a vector
			P = self.last_P
			if self.last_P is None:
				P = self.Phi(self.last_state)

			v_current = sum(sum(self.w*P))
			v_next = sum(sum(self.w*P_))

			delta = self.last_reward + self.gamma * v_next - v_current
			self.average_reward += self.n * delta

			self.w += self.a_w * self.gamma * delta * P

			log_pi_grad = (self.last_action - mu) * P / self.sigma ** 2
			self.theta += self.a_theta * self.gamma * delta * log_pi_grad

			# Let's optimize a little bit and reuse this P
			self.last_P = P_

		return np.random.normal(mu, self.sigma)

	def reward(self, observation, action, reward):

		# Update the average reward
		self.average_reward = (self.average_reward * self.step + reward) / (self.step + 1)

		self.last_action = action
		self.last_reward = reward
		self.last_state = observation

Agent = ActorCriticPolicyGradientAgent
