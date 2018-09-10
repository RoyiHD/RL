from random import  random, choice

class AI:

    def __init__(self, actions, Q, alpha=0.1, discount=0.9):

        self.discount = discount
        self.alpha = alpha
        self.actions = actions
        self.Q = Q

    def learn(self, reward, state, action, prev_state):

        return None

    def choose_action(self, state, epsilon):

        return None

    def calculate_total_rewards(self):
        return sum([val for val in self.Q.values()])