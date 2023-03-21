import Environnement
import random as rd
import copy
import math

env = Environnement.Environnement(5,[[1,1],[2,1],[2,2]],[2,3])
#env = Environnement.Environnement(5,[],[2,3])
print(env)
def truncate_data(env,X):
    c = copy.deepcopy(env)
    X_out = []
    for x in X:
        c.one_deplacement_auto(x)
        c.check_etat()
        if c.etat_global:
            X_out.append(x)
        else:
            break
    return(X_out)

def generation_population(env):
    len_pop = 10000
    deplacement = ['z','q','s','d']
    
    pop = []
    
    for k in range(len_pop):
        Xk = [rd.choice(deplacement) for i in range(100)]
        Xk = truncate_data(env,Xk)
        pop.append(Xk)
    
    return pop

pop = generation_population(env)
#print(pop[:3])

def give_score(env,X):
    c = copy.deepcopy(env)
    c.auto_play_from_data(X)
    score_taille = c.serpent.taille
    score_temps = len(X)
    if score_temps==0:
        return([0,0])
    return([score_taille,1/score_temps])
    
    
def give_all_score(env,pop):
    res = []
    for X in pop:
        res.append(give_score(env,X))
    return(res)
    
scores = give_all_score(env,pop)
#print(scores[:3])

def give_best_elements(pop,scores):
    sort = sorted(scores, reverse = True)
    sort = sort[:100]
    l_indices = [scores.index(s) for s in sort]
    res = [pop[k] for k in l_indices]
    return res,sort

be,score = give_best_elements(pop,scores)


def get_proba_mutation(i,longueur):
    ratio = i/longueur - 1
    return(math.exp(ratio)*0.8)



def gen_one_children(env,element):
    n_mut = 0
    longueur = len(element)
    deplacement = ['z','q','s','d']
    children = []
    while n_mut<101:
        i = rd.randint(0,longueur)
        p = get_proba_mutation(i,longueur)
        e = rd.random()
        if e<p:
            n_mut+=1
            #print(i,longueur)
            child = element[:i]
            add = [rd.choice(deplacement) for i in range(100)]
            child = child + add
            child = truncate_data(env,child)
            children.append(child)
    return(children)

#children = gen_children(env,be[0])
#scores = give_all_score(env,children)
#bc,sc = give_best_elements(pop,scores) 
#print(score[0])
#print(sc[:5])
    
def gen_all_children(env,bests):
    all_children = []
    for el in bests:
        children = gen_one_children(env,el)
        for c in children:
            all_children.append(c)
    return(all_children)


def algo_gen(env):
    pop = generation_population(env)
    scores = give_all_score(env,pop)
    be,score = give_best_elements(pop,scores)
    all_children = gen_all_children(env,be)
    max_iter = 100
    for k in range(max_iter):
        print(k)
        scores = give_all_score(env,all_children)
        be,score = give_best_elements(all_children,scores)
        all_children = gen_all_children(env,be)
    be,s = give_best_elements(all_children,scores)
    return(be)
    
best = algo_gen(env)
print(best[:5])
    