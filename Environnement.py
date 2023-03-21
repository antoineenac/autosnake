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
        
    def give_next_croquette(self,num,liste):
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
    
            
    def refresh_env(self):
        for x in range(self.taille):
            for y in range(self.taille):
                if (([x,y] not in self.obstacles) and ([x,y] not in self.serpent.l_coord)):
                    self.env[x,y] = 0
                if ([x,y] in self.obstacles):
                    self.env[x,y] = 1
                if ([x,y] in self.serpent.l_coord):
                    self.env[x,y] = 2
                if [x,y] == self.coord_croquette:
                    self.env[x,y] = 3
    
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
            print(self.serpent.taille)
            #print(self.evaluate_complexity_path())
            self.check_etat()
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


        
        