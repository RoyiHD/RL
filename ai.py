from random import  random, choice

class AI:

    def __init__(self, actions, Q, alpha=0.1, discount=0.9):

        self.discount = discount
        self.alpha = alpha
        self.actions = actions
        self.Q = Q

    def learn(self, reward, state, action, prev_state):

        #STEP 1: Get current value from Q table for (prev_state, action)

        #STEP 2: Get the max value from list of all (state, actions) pairs

        #STEP 3: Apply Q learning of new value

        #STEP 4: Update the (Prev_state, action) in Q table with new value

        #STEP 5: Return new value
        return None

    def choose_action(self, state, epsilon):

        #STEP 1: Get random number and check if bigger than Epsilon, return random action if smaller

        #STEP 2: Get all the values of (state, actions) as list

        #STEP 3: extract max value from list in step 2

        #STEP 4: Check if max value occurs more than once:
            # if so: choose random value from all max values
            #else: get the index of the max value

        #STEP 5: return the action based on the index of the maximum value

        return None

    def calculate_total_rewards(self):
        return sum([val for val in self.Q.values()])