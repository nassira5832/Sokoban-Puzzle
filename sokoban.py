import math
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
    
    def isGoal(self):
        for i , row in enumerate(self.grid):
            for j , cell in enumerate(row): 
                if (cell=='*'):
                    cmpt+=1
        for row in self.grid:
            for cell in row:
                if cell == 'B' and cmpt==0 :
                    print("il n'existe pas de box dans votre grid ")
                else : return False    
        return True
      
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
    def manhattan_distance(self, box, target):
        box_x, box_y = box
        target_x, target_y = target
        return abs(box_x - target_x) + abs(box_y - target_y)
    def h1(self):
        somme=0
        for row in self.grid:
            for cell in row:
                if cell == 'B' :
                    somme=+1
        return somme 
    def h2(self):
        h1_value = self.h1()
        manhattan_sum = 0
        for box in self.boxes():
                min_distance = min(self.manhattan_distance(box, target) 
                                               for target in self.get_targets())
                manhattan_sum += min_distance

        return 2 * h1_value + manhattan_sum 
    def distance_euclidienne(self, box , target): 
        box_x, box_y=box 
        target_x, target_y=target 
        return math.sqrt((box_x - target_x) ** 2 + (box_y - target_y) ** 2)
    def h3(self):
        h=0
        max_distance = math.sqrt(len(self.grid) ** 2 + len(self.grid[0]) ** 2)
        for box in self.boxes:
            min_dist = min( self.distance_euclidienne(box, target) * (1 + self.distance_euclidienne(box, target) / max_distance)for target in self.targets)
            h += min_dist
        return h


    


class Node :
    def __init__(self, state, parent, action, g=0 ):
        self.state = state
        self.parent=parent 
        self.action=action
        if parent is None:
            self.g = g
        else:
            self.g = parent.g + 1
        self.h=0
        self.f= self.g + self.h
        
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

def BFS(initial_state):
    queue = Queue() 
    visited = set()
    queue.enqueue(Node(initial_state, None, None))
    visited.add(initial_state)
    while not queue.is_empty():
        current_node = queue.dequeue()
        if current_node.state.isGoal():
            return current_node.getSolution()  
        for action, newGrid  in current_node.state.successorFunction():
            if newGrid not in visited:
                new_node = Node(newGrid, current_node, action)
                queue.enqueue(new_node)
                visited.add(newGrid)
        return None



def AStar (initial_state ):
    queue = Queue() 
    visited = set()
    initial_node=(Node(initial_state, None, None))
    queue.enqueue((initial_node.f, initial_node))
    initial_node.setF(0)
    visited.add(initial_state)
    while not queue.is_empty():
        current_node = queue.dequeue()
        if current_node.state.isGoal():
            return current_node.getSolution()  
        for action, newGrid  in current_node.state.successorFunction():
            if newGrid not in visited:
                new_node = Node(newGrid, current_node, action)
                h1 = new_node.state.h1()  
                h2 = new_node.state.h2()
                new_node.setF(h2)
                queue.enqueue((new_node.f, new_node))
                visited.add(newGrid)
    return None


# A* avec Distance Euclidienne
def AStar (initial_state ):
    queue = Queue() 
    visited = set()
    initial_node=(Node(initial_state, None, None))
    queue.enqueue((initial_node.f, initial_node))
    initial_node.setF(0)
    visited.add(initial_state)
    while not queue.is_empty():
        current_node = queue.dequeue()
        if current_node.state.isGoal():
            return current_node.getSolution()  
        for action, newGrid  in current_node.state.successorFunction():
            if newGrid not in visited:
                new_node = Node(newGrid, current_node, action)
                h3 = new_node.state.h3()
                new_node.setF(h3)
                queue.enqueue((new_node.f, new_node))
                visited.add(newGrid)
    return None





        
        
        




