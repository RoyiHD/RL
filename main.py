from matplotlib import pyplot as plt
from env import MouseMaze
from ai import AI
import utils
import time

START_e = 0.99
END_e = 0.0004

def run(env, ai, train):

    state = env.get_state()
    epsilon = START_e if len(ai.Q) <= 0 else END_e
    if not train:
        epsilon = -1

    iter = 0
    rewards = []
    epsilons = []
    sleep_time = 1.0

    while "luke" != "last_jedi":


        action = ai.choose_action(state, epsilon)
        new_state, reward, status = env.get_frame_step(ai, state, action=action)

        if epsilon > END_e:
            epsilon -= END_e

        #calculating new q value based on new state
        q_val = ai.learn(reward, new_state, action, state)

        #Updating text to show values
        env.updateText(q_val, state, new_state, action)

        env.updateScreen()


        if iter % 50 == 0:
            utils.save_j(ai.Q, 'resources/q.json')
            utils.save_j(env.values, 'resources/values.json')
            sum_rewards = ai.calculate_total_rewards()
            rewards.append(sum_rewards)
            epsilons.append(epsilon)
            utils.save_j({'rewards':rewards, 'epsilon':epsilons}, 'resources/data.json')
            print("Iter %d Accumulated Rewards %f with Epsilon %f" % (iter, sum_rewards , epsilon))

        state = new_state
        iter += 1
        if status:
            state = env.reset()

        key = env.run()
        if key:
            if key == 102:
                sleep_time -= 0.25
            elif key == 115: #(S key)
                sleep_time += 0.25

        time.sleep(sleep_time)


def plot_stuff():
    data = utils.load_j('resources/data.json')
    rewards, epsilon = data['rewards'], data['epsilon']

    #print(rewards)
    plt.subplot(2,1,1)
    plt.plot(rewards)
    plt.ylabel('rewards')
    plt.xlabel('iterations (hundreds)')

    plt.subplot(2, 1, 2)
    plt.plot(epsilon)
    plt.ylabel('epsilon')
    plt.xlabel('iterations (hundreds)')

    plt.show()



if __name__ == "__main__":

    #plot_stuff()
    ai = AI(utils.load_j('resources/q.json'))
    game = MouseMaze(utils.load_j('resources/values.json'))
    run(game, ai, True)