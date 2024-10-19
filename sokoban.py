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
                if (cell=='R' or cell=='.'):
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
        
    def successorFunction(self):
        successors = [] 
        x , y = self.find_player()

        directions = {
        'UP': (-1, 0),
        'DOWN': (1, 0),
        'LEFT': (0, -1),
        'RIGHT': (0, 1)
        }
        for i, (dx,dy) in directions.items():
            newX= x+dx
            newY=y+dy 
            if (0 <= newX < len(self.grid) and 0 <= newY< len(self.grid[0]) and self.grid[newX, newY]!='O' and self.grid[newX, newY]!='*'):
                if (self.grid[newX, newY]=='S'):
                    newGrid = [row[:] for row in self.grid]
                    newGrid[x,y]=''
                    newGrid[newX, newX]='.'
                    successors.append((i, newGrid))

                if (self.grid[newX, newY]==''):
                    newGrid = [row[:] for row in self.grid]
                    newGrid[x,y]=''
                    newGrid[newX, newX]='R'
                    successors.append((i, newGrid))

                if(self.grid[newX, newY]=='B' ):
                    if (0 <= newX+dx < len(self.grid) and 0 <= newY+dy< len(self.grid[0]) and self.grid[newX+dx, newY+dy]!='O' and self.grid[newX+dx, newY+dy]!='*'and self.grid[newX+dx, newY+dy]!='B'):
                     
                     if(self.grid[newX+dx, newY+dy]==''):
                        newGrid = [row[:] for row in self.grid]
                        newGrid[x,y]=''
                        newGrid[newX, newX]='R'
                        newGrid[newX+dx, newY+dy]='B'
                        successors.append((i, newGrid))
                    
                     if(self.grid[newX+dx, newY+dy]=='S'):
                        newGrid = [row[:] for row in self.grid]
                        newGrid[x,y]=''
                        newGrid[newX, newX]='R'
                        newGrid[newX+dx, newY+dy]='*'
                        successors.append((i, newGrid))
        return successors
class Node :
    def __init__(self, state, parent, action, g=0):
        self.state = state
        self.parent=parent 
        self.action=action
        if parent is None:
            self.g = g
        else:
            self.g = parent.g + 1
        
        
    def getPath (self): 
        path=[]
        current = self
        while current is not None :
            path.append(current.state)
            current=current 
        return path
    def getSolution (self):
        actions=[]
        current = self
        while current is not None :
            actions.append(current.action)
            current=current.parent
        return actions 
    def setF(self, h):
        self.h = h
        self.f = self.g + self.h


    
            



    

        

        






            


                                                                     

    
                
                


        
    
