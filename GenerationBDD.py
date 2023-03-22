import AlgoGen
import Environnement
import copy
import random as rd


def get_differents(pop):
    all_diff = []
    seen = []
    for x in pop:
        if not x in seen:
            all_diff.append(x)
            seen.append(x)
    return all_diff
            

def gen_database_from_env(env):
    copy_env = copy.deepcopy(env)
    best,s = AlgoGen.algo_gen(copy_env)
    differents_best = get_differents(best)
    Xs,Ys = [], []
    for play in differents_best:
        c = copy.deepcopy(env)
        for inputs in play:
            envi = copy.deepcopy(c.env)
            Xs.append(envi)
            Ys.append(inputs)
            c.one_deplacement_auto(inputs)
            c.check_etat()
            c.refresh_env()
    return(Xs,Ys)    
    
#Xs,Ys = gen_database_from_env(env)
#print(Xs[:3])
#print(Ys[:3])

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


def generation_database(nombre_env,taille):
    X = []
    Y = []
    
    for i in range(nombre_env):
        print(i)
        env = generation_environnements(taille)
        Xs,Ys = gen_database_from_env(env)
        for x in Xs:
            X.append(x)
        for y in Ys:
            Y.append(y)
        
    return(X,Y)
    
X,Y = generation_database(2,5)

