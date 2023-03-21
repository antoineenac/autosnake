class Serpent():
    def __init__(self,coord_start):
        self.taille = 1
        self.l_coord = [coord_start]
        self.coord_head = self.l_coord[0]
    
    def deplacement(self,direction,flag_croquette):
        if not flag_croquette:
            if direction=="up":
                next_coord = [self.coord_head[0]-1,self.coord_head[1]]
                self.coord_head = next_coord
                self.l_coord.pop(-1)
                self.l_coord = [next_coord] + self.l_coord
            if direction == "down":
                next_coord = [self.coord_head[0]+1,self.coord_head[1]]
                self.coord_head = next_coord
                self.l_coord.pop(-1)
                self.l_coord = [next_coord] + self.l_coord
            if direction == "left":
                next_coord = [self.coord_head[0],self.coord_head[1]-1]
                self.coord_head = next_coord
                self.l_coord.pop(-1)
                self.l_coord = [next_coord] + self.l_coord
            if direction == "right":
                next_coord = [self.coord_head[0],self.coord_head[1]+1]
                self.coord_head = next_coord
                self.l_coord.pop(-1)
                self.l_coord = [next_coord] + self.l_coord
        else:
            if direction=="up":
                next_coord = [self.coord_head[0]-1,self.coord_head[1]]
                self.coord_head = next_coord
                self.l_coord = [next_coord] + self.l_coord
                self.taille += 1
            if direction == "down":
                next_coord = [self.coord_head[0]+1,self.coord_head[1]]
                self.coord_head = next_coord
                self.l_coord = [next_coord] + self.l_coord
                self.taille += 1
            if direction == "left":
                next_coord = [self.coord_head[0],self.coord_head[1]-1]
                self.coord_head = next_coord
                self.l_coord = [next_coord] + self.l_coord
                self.taille += 1
            if direction == "right":
                next_coord = [self.coord_head[0],self.coord_head[1]+1]
                self.coord_head = next_coord
                self.l_coord = [next_coord] + self.l_coord
                self.taille += 1
        

