#from matplotlib import pyplot as plt
from random import  random, choice
from env import MouseMaze
from ai import AI
import utils
import time

START_e = 0.99
DECAY = 0.0003

def run(env, ai, train):

    state = env.get_state()
    epsilon = START_e if len(ai.Q) <= 0 else -1
    if not train:
        epsilon = -1

    iter = 0
    rewards = []
    epsilons = []
    sleep_time = 1.0
    paused = False

    while "LUKE" != "LAST_JEDI":
        env.updateScreen()
        key = env.run()
        if key:
            if key == 102:  # (F KEY)
                if sleep_time >= 0.25:
                    sleep_time -= 0.25
            elif key == 115:  # (S key)
                sleep_time += 0.25
            elif key == 101: # (E key) END GAME
                break
            elif key == 100:  # (D key) PAUSE GAME
                if paused:
                    paused = False
                else:
                    paused = True

        if paused:
            continue

        # STEP 1: Choose Action
        action = ai.choose_action(state, epsilon)
        #action = env.varify_action(action)

        # STEP 2: Get New State, Reward, Status
        new_state, reward, status = env.get_frame_step(ai, state, action)
        # STEP 3: Train
        q_val = ai.learn(reward, new_state, action, state)

        # Step 4 Updating text to show values
        env.updateText(q_val, state, new_state, action)


        # STEP 5: Change state to new state
        state = new_state

        if status:
            state = env.reset()

        if epsilon > 0:
            epsilon -= DECAY

        iter += 1
        if iter % 50 == 0:
            sum_rewards = ai.calculate_total_rewards()
            rewards.append(sum_rewards)
            epsilons.append(epsilon)
            utils.save_j(ai.Q, 'resources/q.json')
            utils.save_j(env.values, 'resources/values.json')
            utils.save_j({'rewards':rewards, 'epsilon':epsilons}, 'resources/data.json')
            print("Iter %d Accumulated Rewards %f with Epsilon %f" % (iter, sum_rewards , epsilon))

        time.sleep(sleep_time)

'''
def plot_stuff():
    data = utils.load_j('resources/data.json')
    rewards, epsilon = data['rewards'], data['epsilon']

    plt.subplot(2,1,1)
    plt.plot(rewards)
    plt.ylabel('rewards')
    plt.xlabel('iterations (hundreds)')

    plt.subplot(2, 1, 2)
    plt.plot(epsilon)
    plt.ylabel('epsilon')
    plt.xlabel('iterations (hundreds)')

    plt.show()
'''

if __name__ == "__main__":

    #plot_stuff()
    actions = ["LEFT", "RIGHT", "UP", "DOWN"]
    ai = AI(actions, utils.load_j('resources/q.json'))
    game = MouseMaze(actions, utils.load_j('resources/values.json'))
    run(game, ai, True)