from random import  random, choice

class AI:

    def __init__(self, Q, epsilon=0.15, alpha=0.05, discount=0.99):

        self.epsilon = epsilon
        self.alpha = alpha
        self.discount = discount
        self.START_E = epsilon
        self.END_E = 0.05
        self.actions = ["LEFT", "RIGHT", "UP", "DOWN"]
        self.Q = Q


    def learn(self, reward, state, action, prev_state):

        _max_val = max([self.Q.get(("%s-%s"% (state, i)), 0.0)for i in self.actions])
        _val = self.Q.get(("%s-%s" % (prev_state, action)), 0.0)
        new_val = _val + self.alpha * (reward + (self.discount * _max_val) - _val)
        self.Q[("%s-%s" % (prev_state, action))] = new_val

        return new_val

    def choose_action(self, state, epsilon):

        if random() < epsilon:
            return choice(self.actions)

        actions = [self.Q.get(("%s-%s" % (state,i)), 0.0) for i in self.actions]
        _max = max(actions)

        if actions.count(_max) > 0:
            index =  choice([i for i in range(len(self.actions)) if actions[i] == _max])
        else:
            index = actions.index(_max)

        return self.actions[index]

    def calculate_total_rewards(self):
        return sum([val for val in self.Q.values()])