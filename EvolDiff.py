   
    
def get_Trial(pop,i,taille_pop):
    F = 1
    CR = 0.5
    r1,r2,r3 = rd.randint(0,taille_pop-1),rd.randint(0,taille_pop-1),rd.randint(0,taille_pop-1)
    while(r1==r2 or r1==r3 or r2==r3 or r1==i or r2==i or r3==i):
        r1,r2,r3 = rd.randint(0,taille_pop-1),rd.randint(0,taille_pop-1),rd.randint(0,taille_pop-1)
    M = [((pop[r1][k] + F*(pop[r2][k] - pop[r3][k])) % (2*math.pi)) for k in range(len(pop[i]))]
    Trial_i = []
    for j in range(len(pop[i])):
        random = rd.random()
        if random<CR:
            Trial_i.append(M[j])
        else:
            Trial_i.append(pop[i][j])
            
    return(Trial_i)
    
def gen_random_x(env):
    flag = False
    while not flag:
        c = copy.deepcopy(env)
        res = [rd.uniform(0,2*math.pi) for k in range(10)]
        for x in res:
            c.one_deplacement_auto(x)
            c.check_etat()
            if not c.etat_global:
                break
        if c.etat_global:
            return(res)
        
    
    

def one_step_evol_diff(pop,env):
    c = copy.deepcopy(env)
    for i in range(len(pop)):
        Trial_i = get_Trial(pop,i,len(pop))
        score_Trial = get_score_10_step(Trial_i,env)
        
        X_i = pop[i]
        score_X = get_score_10_step(X_i,env)
        
        if score_Trial > score_X:
            for x in Trial_i:
                c.one_deplacement_auto(x)
                c.check_etat()
                if not c.etat_global:
                    break
            if c.etat_global:
                X_i = Trial_i
            

def get_best_score(pop,env):
    best = -100000
    x_best = pop[0]
    for x in pop:
        aux = get_score_10_step(x,env)
        if aux>best:
            best = aux
            x_best = x
    return(best,x_best)
            
            
            
def evol_diff(env):
    len_pop = 1000
    print("gen pop")
    pop = [gen_random_x(env) for k in range(len_pop)]
    print("gen pop ok")
    i=0
    n_iter = 2000
    while(i<n_iter):
        if i%100==0:
            print(str(i)+"\n")
        i+=1
        one_step_evol_diff(pop,env)
        #print(get_best_score(pop,env)[0])
        #print("\n")
    best,x_best = get_best_score(pop,env)
    
    return best,x_best

def conversion(X):
    X_sent = []
    for x in X:
        if (x<math.pi/8 or x>7*math.pi/4):
            X_sent.append("d")
        if (x>math.pi/4 or x<3*math.pi/4):
            X_sent.append("z")
        if (x>3*math.pi/4 or x<5*math.pi/4):
            X_sent.append("q")
        if (x>5*math.pi/4 or x<7*math.pi/4):
            X_sent.append("s")
    return X_sent    
    
def one_step_auto_play(env):
    up_env = copy.deepcopy(env)
    down_env = copy.deepcopy(env)
    left_env = copy.deepcopy(env)
    right_env = copy.deepcopy(env)
    
    up_env.one_deplacement_auto("z")
    ev_up = Evaluation.get_evaluation(up_env)
    up_env.check_etat()
    if not up_env.etat_global:
        ev_up = -1
    
    down_env.one_deplacement_auto("s")
    ev_down = Evaluation.get_evaluation(down_env)
    down_env.check_etat()
    if not down_env.etat_global:
        ev_down = -1
    
    left_env.one_deplacement_auto("q")
    ev_left = Evaluation.get_evaluation(left_env)
    left_env.check_etat()
    if not left_env.etat_global:
        ev_left = -1
    
    right_env.one_deplacement_auto("d")
    ev_right = Evaluation.get_evaluation(right_env)
    right_env.check_etat()
    if not right_env.etat_global:
        ev_right = -1
    
    aux = [ev_up,ev_down,ev_left,ev_right]
    m = max(aux)
    i_m = aux.index(m)
    
    if i_m==0:
        print("z")
        env.one_deplacement_auto("z")
    if i_m==1:
        print("s")
        env.one_deplacement_auto("s")
    if i_m==2:
        print("q")
        env.one_deplacement_auto("q")
    if i_m==3:
        print("d")
        env.one_deplacement_auto("d")
        
def auto_play(env):
    i=0
    while i<100:
        print(env.env)
        one_step_auto_play(env)
        env.check_etat()
        if not env.etat_global:
            break
        env.refresh_env()
        i+=1
        time.sleep(2)
    if env.etat_global:
        print("you won")
    else:
        print("you lost")
        
        
        
        
def get_score_10_step(X,env):
    copy_env = copy.deepcopy(env)
    X_sent = []
    for x in X:
        if (x<math.pi/8 or x>7*math.pi/4):
            X_sent.append("d")
        if (x>math.pi/4 or x<3*math.pi/4):
            X_sent.append("z")
        if (x>3*math.pi/4 or x<5*math.pi/4):
            X_sent.append("q")
        if (x>5*math.pi/4 or x<7*math.pi/4):
            X_sent.append("s")
    for x in X_sent:
        copy_env.one_deplacement_auto(x)
        if not copy_env.etat_global:
            break
    if copy_env.etat_global:
        return(Evaluation.get_evaluation(copy_env))
    else:
        return -100