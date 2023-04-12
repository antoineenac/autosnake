import numpy as np
import random as rd
import copy
import time
import os
import math


import Serpent
import Evaluation 


class Environnement():
    def __init__(self,taille,coord_obstacles,coord_start):
        self.taille = taille
        self.env = np.array([[0 for k in range(self.taille)] for i in range(self.taille)]) #carte carrée de coté self.taille
        
        self.obstacles = coord_obstacles #liste des coordonnées des obstacles, les coordonnées sont de la forme [x,y], avec x,y des entiers

        self.serpent = Serpent.Serpent(coord_start)

        self.etat_global = True
        
        #self.coord_croquette = self.give_cood_croquette()
        #self.coord_croquette = [2,2]
        
        self.numero_croquette = 0
        self.liste_all_croquettes = [[2, 0],[4, 2],[0, 4], [4, 3], [1, 0], [2, 4], [1, 2], [0, 0], [1, 2], [0, 0], [2, 4], [4, 0], [1, 3],[0, 3], [4, 0],[4, 4], [0, 1], [4, 3], [1, 0], [4, 3]]
        
        self.coord_croquette = self.give_next_croquette(self.numero_croquette,self.liste_all_croquettes)
        
        self.flag_croquette = False
        
        self.refresh_env()
        
        self.q_etat = self.get_q_etat() #for q learning
        
    def get_q_etat(self):
        x_head,y_head = self.serpent.coord_head[0],self.serpent.coord_head[1]
        
        check_up = 1
        if ([x_head - 1,y_head] in self.obstacles or [x_head - 1,y_head] in self.serpent.l_coord[1::]):
            check_up = 0
        check_down = 1
        if ([x_head + 1,y_head] in self.obstacles or [x_head + 1,y_head] in self.serpent.l_coord[1::]):
            check_down = 0
        check_left = 1
        if ([x_head,y_head - 1] in self.obstacles or [x_head,y_head - 1] in self.serpent.l_coord[1::]):
            check_left = 0
        check_right = 1
        if ([x_head,y_head + 1] in self.obstacles or [x_head,y_head + 1] in self.serpent.l_coord[1::]):
            check_right = 0
        
        check_vec = [check_up,check_down,check_right,check_left]
        
        def check_direction(head,before_head):
            xh,yh = head[0],head[1]
            
            if len(before_head)<2:
                return 'none'
            x_bh,y_bh = before_head[1][0],before_head[1][1]
            
            dx = xh - x_bh
            dy = yh - y_bh
            
            if dx==1:
                return 'down'
            if dx==-1:
                return 'up'
            if dy==1:
                return 'right'
            if dy==-1:
                return 'left'
        
        direction = check_direction(self.serpent.coord_head,self.serpent.l_coord)
        
        gone_up,gone_down,gone_left,gone_right = 0,0,0,0
        if direction=='up':
            gone_up = 1
        if direction=='down':
            gone_down = 1
        if direction=='right':
            gone_right = 1
        if direction=='left':
            gone_left = 1
            
        gone_vec = [gone_up,gone_down,gone_left,gone_right]
            
        def croquette_direction(head,croquette):
            xh,yh = head[0],head[1]
            xc,yc = croquette[0],croquette[1]
            
            dx = xh - xc
            dy = yh - yc
            
            if dx==0:
                if dy==0:
                    return 0,0,0,0
                if dy>0:
                    return 1,0,0,0
                if dy<0:
                    return 0,1,0,0
            
            if dx>0:
                if dy==0:
                    return 0,0,0,1
                if dy>0:
                    return 1,0,0,1
                if dy<0:
                    return 0,1,0,1
            else:
                if dy==0:
                    return 0,0,1,0
                if dy>0:
                    return 1,0,1,0
                if dy<0:
                    return 0,1,1,0
        
        going_left,going_right,going_down,going_up = croquette_direction(self.serpent.coord_head,self.coord_croquette)
        going_vec = [going_up,going_down,going_right,going_left]
        
        
        return(check_vec + gone_vec + going_vec)
        #return(check_vec + going_vec)
        
            
    def give_next_croquette(self,num,liste):
        while(liste[num] in self.serpent.l_coord):
            num+=1
        return(liste[num])
        
    def give_cood_croquette(self):
        x,y = rd.randint(0,self.taille-1),rd.randint(0,self.taille-1)
        
        while  ([x,y] in self.obstacles or [x,y] in self.serpent.l_coord):
            x,y = rd.randint(0,self.taille-1),rd.randint(0,self.taille-1)
            
        return [x,y]
            
    
    def __repr__(self):
        os.system('cls')
        return(str(self.env))
        
        
        
    def one_deplacement(self):
        flag = self.flag_croquette
        dep = input("deplacement : ")
        if dep=="z":
            self.serpent.deplacement("up",flag)
        if dep=="q":
            self.serpent.deplacement("left",flag)
        if dep=="s":
            self.serpent.deplacement("down",flag)
        if dep=="d":
            self.serpent.deplacement("right",flag)
        if dep == "k":
            self.etat_global=False
        if dep=="wc":
            print(self.coord_croquette)
            
    def one_deplacement_auto(self,key):
        flag = self.flag_croquette
        if key=="z":
            self.serpent.deplacement("up",flag)
        if key=="q":
            self.serpent.deplacement("left",flag)
        if key=="s":
            self.serpent.deplacement("down",flag)
        if key=="d":
            self.serpent.deplacement("right",flag)
        if key == "k":
            self.etat_global=False
        if key=="wc":
            print(self.coord_croquette)
            
    def check_etat(self):
        coord_head = self.serpent.coord_head
        x,y = coord_head[0],coord_head[1]
        if [x,y]==self.coord_croquette:
            self.flag_croquette = True
            self.numero_croquette += 1
            self.coord_croquette = self.give_next_croquette(self.numero_croquette,self.liste_all_croquettes)
            #print(self.coord_croquette)
        else:
            self.flag_croquette = False
        if (x<0 or x>self.taille-1):
            self.etat_global = False
        else:
            if (y<0 or y>self.taille-1):
                self.etat_global = False
            else:
                if [x,y] in self.obstacles:
                    self.etat_global = False
                else:
                    if [x,y] in self.serpent.l_coord[1::]:
                        self.etat_global = False
        self.q_etat = self.get_q_etat()
    
            
    def refresh_env(self):
        for x in range(self.taille):
            for y in range(self.taille):
                if (([x,y] not in self.obstacles) and ([x,y] not in self.serpent.l_coord)):
                    self.env[x,y] = 0
                if ([x,y] in self.obstacles):
                    self.env[x,y] = 1
                if ([x,y] in self.serpent.l_coord):
                    self.env[x,y] = 2
                if ([x,y] == self.serpent.coord_head):
                    self.env[x,y] = 3
                if [x,y] == self.coord_croquette:
                    self.env[x,y] = -1
    
    def auto_play_from_data(self,X):
        for x in X:
            self.one_deplacement_auto(x)
            self.check_etat()
            self.refresh_env()
                
    def boucle(self):
        i=0
        while i<100:
            print(self.env)
            self.one_deplacement()
            #print(self.serpent.taille)
            self.check_etat()
            print(self.q_etat)
            if not self.etat_global:
                break
            self.refresh_env()
            i+=1
        if self.etat_global:
            print("you won")
        else:
            print("you lost")
            
            
            
            
#env = Environnement(5,[[1,1],[2,1],[2,2]],[2,3])
#env.boucle()


        
        