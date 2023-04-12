import Environnement

import numpy as np
import math

import matplotlib.pyplot as plt


env = Environnement.Environnement(5,[[1,1],[2,1],[2,2]],[2,3])

nb_states = int(math.pow(2,len(env.q_etat)))
nb_actions = 4


def get_number_state(state):
    b = 1
    s = 0
    for n in state:
        s += n*b
        b = b*2
    return n

def init_Qtable(nb_states,nb_actions):
    return(np.zeros((nb_states,nb_actions)))
       
Qtable = init_Qtable(nb_states,nb_actions)


def train(n_episodes, max_steps,Q, gamma=0.2, epsilon=0.3, alpha=0.2):
    all_rewards = []
    for episode in range(n_episodes):
# Reset the environment pour avoir l'état de départ s 
        env = Environnement.Environnement(5,[],[2,3])
        state = env.q_etat
        total = 0
        for step in range(max_steps):
            # choisir une action a avec la stratégie epsilon greedy
            p = np.random.binomial(1,epsilon)
            if not p: 
                action = np.random.choice(["z","s","d","q"])
            else:
                i_state = get_number_state(state)
                i_action = np.argmax(Q[i_state])
                l_action = ["z","s","d","q"]
                #print(i_action)
                action = l_action[i_action]
                        
            # faire l'action et récupérer le résultat 
            #observation, reward, done, truncated, info = env.step(action)
            env.one_deplacement_auto(action)
            done = False
            if env.serpent.coord_head == env.coord_croquette:
                reward = 100
            else: 
                reward = -1
            env.check_etat()
            env.refresh_env()
            if not env.etat_global:
                reward = -100
                total+= reward
                done = True
            
            
            total += reward
            statep = env.q_etat
            # mise à jour de Q(s,a) 
            
            i_state = get_number_state(state)
            i_statep = get_number_state(statep)
            
            l_action = ["z","s","d","q"]
            #print(action)
            i_action = l_action.index(action)
            
            Q[i_state][i_action] = (1 - alpha)*Q[i_state][i_action] + alpha*(reward + gamma*max(Q[i_statep]))
            
            state = statep
            
            if done:
                break
        all_rewards.append(total)
    return Q,all_rewards


Qtable,rew = train(2000,500,Qtable)
print(Qtable)
plt.plot(rew)