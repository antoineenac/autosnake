import Basic_Neural_Netwok
import Environnement
import copy
import random as rd
import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout

from tensorflow.keras.models import load_model


model = load_model('neural_network.h5')


def give_score(env,X):
    c = copy.deepcopy(env)
    c.auto_play_from_data(X)
    score_taille = c.serpent.taille
    score_temps = len(X)
    if score_temps==0:
        return([0,0])
    return([score_taille,1/score_temps])


def get_one_party(envir):
	
	Xs,Xs_nn,Ys = [],[],[]
	
	env = copy.deepcopy(envir)
	
	while env.etat_global:
		input_nn = env.q_etat
		Xs_nn.append(input_nn)
		
		envi = copy.deepcopy(env.env)
		Xs.append(envi)
		
		pred = model.predict([input_nn],verbose=0)[0]
		plays = ["z","s","q","d"]
		next_play = plays[list(pred).index(rd.choices(pred,pred))]
		Ys.append(next_play)
		
		env.one_deplacement_auto(next_play)
		env.check_etat()
		env.refresh_env()
		
		

	
	score = give_score(envir,Ys)
	
	return(Xs,Xs_nn,Ys,score)
	

def get_batch_from_env(env,nbr_elt):
	batch = []
	
	for k in range(nbr_elt):
		envi = copy.deepcopy(env)
		X,X_nn,Y,score = get_one_party(envi)
		batch.append([X,X_nn,Y,score])
		
	return batch
	


def gen_database_from_env_nn(env,nombre_env):
	copy_env = copy.deepcopy(env)
	batch = get_batch_from_env(copy_env,nombre_env)
	best_batches = sorted(batch,key = lambda x : x[-1], reverse = True)[:int(len(batch)/4)]
	
	X,X_nn,Y = [],[],[]
	for elt in best_batches:
		X = X+elt[0]
		X_nn = X_nn+elt[1]
		Y = Y + elt[2]
		
	return(X,X_nn,Y)
    
def generation_environnements(taille):
    
    def generation_obstacles(taille,nombres):
        l_obst = []
        for k in range(nombres):
            x,y = rd.randint(0,taille-1),rd.randint(0,taille-1)
            l_obst.append([x,y])
        return l_obst
    nombre_obstacles = rd.randint(0,taille)
    l_obstacles = generation_obstacles(taille, nombre_obstacles)
    
    def generation_liste_croquettes(taille, l_obstacles):
        l_croq = []
        for k in range(100):
            x,y = rd.randint(0,taille-1),rd.randint(0,taille-1)
            while [x,y] in l_obstacles:
                x,y = rd.randint(0,taille-1),rd.randint(0,taille-1)
            l_croq.append([x,y])
        return l_croq
    l_croquette = generation_liste_croquettes(taille, l_obstacles)
    #print(l_croquette)
    
    def get_starting_point(taille, l_croq, l_obst):
        x,y = rd.randint(0,taille-1),rd.randint(0,taille-1)
        while [x,y] in l_obst or [x,y] != l_croq[0]:
            x,y = rd.randint(0,taille-1),rd.randint(0,taille-1)
        return [x,y]
    start = get_starting_point(taille, l_croquette, l_obstacles)
    
    env = Environnement.Environnement(taille,l_obstacles,start)
    env.liste_all_croquettes = l_croquette[1::]
    env.coord_croquette = l_croquette[0]
    env.refresh_env()
    
    return env	
	
def generation_database_nn(nombre_env,taille):
    X = []
    X_nn = []
    Y = []
    
    for i in range(nombre_env):
        print(i)
        env = generation_environnements(taille)
        Xs,Xs_nn,Ys = gen_database_from_env_nn(env,100)
        X.append(Xs)
        X_nn.append(Xs_nn)
        Y.append(Ys)
        
    return(X,X_nn,Y)


X,X_nn,Y = generation_database_nn(2,7)
X = np.array(X,dtype=list)
X_nn = np.array(X_nn,dtype=list)
Y = np.array(Y,dtype=list)
np.save("X_2.npy",X)
np.save("X_nn_2.npy",X_nn)
np.save("Y_2.npy",Y)
