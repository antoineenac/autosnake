import numpy as np
import Astar

def evaluate_entortillement(l_coord):
    #l_coord = self.serpent.l_coord
    def alignement_3_cases(c1,c2,c3):
        if c1[0]==c2[0]==c3[0]:
            return 1
        else:
            if c1[1]==c2[1]==c3[1]:
                return 1
            else:
                return 0
    if len(l_coord)<3:
        return 1
    else:
        compteur = 0
        for k in range(len(l_coord)-2):
            compteur += alignement_3_cases(l_coord[k],l_coord[k+1],l_coord[k+2])
        compteur = compteur/(len(l_coord)-2)
        return(compteur)
        
def evaluate_nombre_direction(head_coord,obstacles,l_coord,taille):
    #head_coord = self.serpent.coord_head
    compt = 4
    xh,yh = head_coord[0],head_coord[1]
    
    def check_alentour(x,y):
        return(([x,y] in obstacles) or ([x,y] in l_coord) or (x<0 or x>=taille) or (y<0 or y>=taille))
    
    if check_alentour(xh-1,yh):
        compt -= 1
    if check_alentour(xh+1,yh):
        compt -= 1
    if check_alentour(xh,yh-1):
        compt -= 1
    if check_alentour(xh,yh+1):
        compt -= 1
    return(compt/4)
    

def evaluate_distance_to_croquette(coord_croquette,coord_head,taille):
    
    def biggest_distance(xc,yc):
        dx = max([taille-xc,xc])
        dy = max([taille-yc,yc])
        return(dx+dy)
    xc,yc = coord_croquette[0],coord_croquette[1]
    bd = biggest_distance(xc,yc)
    
    x,y = coord_head[0],coord_head[1]
    distance_to_croquette = abs(xc - x) + abs(yc - y)
    
    ratio = 1 - (distance_to_croquette/bd)
    return(ratio)
    
def evaluate_complexity_path(obstacles,l_coord,taille,coord_croquette,coord_head):
    def convert_env_for_Astar():
        env_Astar = np.array([[0 for k in range(taille)] for i in range(taille)])
        for x in range(taille):
            for y in range(taille):
                if ([x,y] in obstacles):
                    env_Astar[x,y] = 1
                if ([x,y] in l_coord):
                    env_Astar[x,y] = 1
        return(env_Astar)
    env_Astar = convert_env_for_Astar()
    path = Astar.astar(env_Astar, tuple(coord_head), tuple(coord_croquette))
    if path==None:
        return 0
    estimated_length = len(path)
    
    xc,yc = coord_croquette[0],coord_croquette[1]        
    x,y = coord_head[0],coord_head[1]
    distance_to_croquette = abs(xc - x) + abs(yc - y)
    
    if estimated_length==0:
        return 1
    else:
        ratio = distance_to_croquette/estimated_length
    return(ratio)
    
def get_evaluation(env):
    entortillement = evaluate_entortillement(env.serpent.l_coord)
    if (len(env.serpent.l_coord) < 5):
        entortillement = 1
    nb_dir = evaluate_nombre_direction(env.serpent.coord_head,env.obstacles,env.serpent.l_coord,env.taille)
    dist_tc = evaluate_distance_to_croquette(env.coord_croquette,env.serpent.coord_head,env.taille)
    compl_path = evaluate_complexity_path(env.obstacles,env.serpent.l_coord,env.taille,env.coord_croquette,env.serpent.coord_head)
    if env.etat_global:
        return(len(env.serpent.l_coord)*entortillement + nb_dir + 10*dist_tc + 2*compl_path)
    else:
        return(-100)
    