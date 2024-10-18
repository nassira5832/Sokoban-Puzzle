class  SokobanPuzzle:
    def __init__(self, grid):
        self.grid=grid
        self.player= self.findplayer()
        self.walls= self.findwalls()
        self.boxes=self.findboxes()
        self.target = self.findtargets()

    def findplayer(self):
        for i , row in enumerate (self.grid): 
            for j, cell in enumerate(row):
                if (cell=='R'):
                    return (i, j)
        return None
    
    def findwalls(self):
        walls=[]
        for i , row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if (cell=='O'):
                    walls.append((i,j))
        return walls
    
    def findboxes (self):
        boxes=[]
        for i , row in enumerate(self.grid):
            for j , cell in enumerate(row):
                if (cell=='B'):
                    boxes.append((i,j))
        return boxes
    
    def findtargets (self): 
        targets =[]
        for i , row in enumerate(self.grid):
            for j , cell in enumerate(row): 
                if (cell=='S'): 
                    targets.append((i,j))
        return targets
    def goal(self):
        cmpt=0
        cmptB=0
        for i , row in enumerate(self.grid):
            for j , cell in enumerate(row): 
                if (cell=='*'):
                    cmpt+=1
                else: 
                    if(cell=='B'):
                        cmptB+=1

        if (cmpt==cmptB):
            return True
        else : 
            return False
        
    def

    
                
                


        
    
