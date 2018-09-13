from random import  random, choice

class AI:

    def __init__(self, actions, Q, alpha=0.1, discount=0.9):

        self.discount = discount
        self.alpha = alpha
        self.actions = actions
        self.Q = Q

    def learn(self, reward, state, action, prev_state):

        # STEP 1: Get current value from Q table for (prev_state, action)
        val = self.Q.get("%s-%s" % (prev_state, action), 0.0)
        # STEP 2: Get the max value from list of all (state, actions) pairs
        max_val = max([self.Q.get("%s-%s" % (state, i), 0.0) for i in self.actions])
        # STEP 3: Apply Q learning of new value
        new_val = val + self.alpha * (reward + (self.discount * max_val) - val)
        # STEP 4: Update the (Prev_state, action) in Q table with new value
        self.Q["%s-%s" % (prev_state, action)] = new_val
        # STEP 5: Return new value
        return new_val

    def choose_action(self, state, epsilon):

        if random() < epsilon:
            return choice(self.actions)
        values = [self.Q.get("%s-%s" % (state, i), 0.0) for i in self.actions]
        max_val = max(values)
        if values.count(max_val) > 1:
            index = choice([i for i in range(len(values)) if values[i] == max_val])
        else:
            index = values.index(max_val)

        return self.actions[index]

    def calculate_total_rewards(self):
        return sum([val for val in self.Q.values()])