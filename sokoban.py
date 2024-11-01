import math
import time 
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
        for row in self.grid:
            for cell in row:
                if cell=='S' or cell=='.' or cell=='B':
                   return False
        return True
    
    def successorFunction(self):
        successors = [] 
        x , y = self.findplayer() 
        directions = {
        'UP': (-1, 0),
        'DOWN': (1, 0),
        'LEFT': (0, -1),
        'RIGHT': (0, 1)
        }
        for i, (dx,dy) in directions.items():
            newX= x+dx
            newY=y+dy 
            if (0 <= newX < len(self.grid) and 0 <= newY< len(self.grid[0]) and self.grid[newX][newY]!='O' and self.grid[newX][newY]!='*'):
                if (self.grid[newX][newY]=='S'):
                    newGrid = [row[:] for row in self.grid]
                    newGrid[x][y]=' '
                    newGrid[newX][newY]='.'
                    successors.append((i, newGrid))

                if (self.grid[newX][newY]==' '):
                    newGrid = [row[:] for row in self.grid]
                    newGrid[x][y]=' '
                    newGrid[newX][newY]='R'
                    successors.append((i, newGrid))

                if(self.grid[newX][newY]=='B' ):
                    if (0 <= newX+dx < len(self.grid) and 0 <= newY+dy< len(self.grid[0]) and self.grid[newX+dx][newY+dy]!='O' and self.grid[newX+dx][newY+dy]!='*'and self.grid[newX+dx][newY+dy]!='B'):
                     
                        if(self.grid[newX+dx][newY+dy]==' '):
                           newGrid = [row[:] for row in self.grid]
                           newGrid[x][y]=' '
                           newGrid[newX][newY]='R'
                           newGrid[newX+dx][newY+dy]='B'
                           successors.append((i, newGrid))

                        if(self.grid[newX+dx][newY+dy]=='S'):
                            newGrid = [row[:] for row in self.grid]
                            newGrid[x][y]=' '
                            newGrid[newX][newY]='R'
                            newGrid[newX+dx][newY+dy]='*'
                            successors.append((i, newGrid))
        return successors
    def manhattan_distance(self, box, target):
        box_x, box_y = box
        target_x, target_y = target
        result=abs(box_x - target_x) + abs(box_y - target_y)
        return result 
    
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
        for box in self.boxes:
            distances = [self.manhattan_distance(box, target) for target in self.target]
            if distances:
              min_distance = min(distances)
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
            distences=[ self.distance_euclidienne(box, target) * (1 + self.distance_euclidienne(box, target) / max_distance)for target in self.target]
            if distences:
               min_dist = min(distences)
               h += min_dist
        return h
    def __str__(self):
        return "\n".join("".join(row) for row in self.grid)

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
            current = current.parent 
        return path

    def getSolution (self):
        actions=[]
        current = self
        while current is not None :
            if current.action is not None:
               actions.append(current.action)
            current=current.parent
        actions.reverse()
        return actions 
    def setF(self, h):
        self.h = h
        self.f = self.g + self.h
    def __str__(self):
        return f"Node(f={self.f}, g={self.g}, h={self.h}, action={self.action})"


def BFS(initial_state):
    queue = [] 
    visited = []
    initial_node = Node(initial_state, None, None)
    queue.append(initial_node)
    visited.append(initial_state)

    while len(queue) > 0:
        current_node = queue.pop()
        if current_node.state.isGoal():
            return current_node.getSolution()  
        for action, newGrid in current_node.state.successorFunction():
            if newGrid not in visited:
                new_state = SokobanPuzzle(newGrid)  
                new_node = Node(new_state, current_node, action)
                queue.append(new_node)
                visited.append(new_state)

    return []

def AStar(initial_state):
    queue = [] 
    visited = []
    initial_node = Node(initial_state, None, None)
    h1 = initial_node.state.h1()  
    initial_node.setF(h1) 
    queue.append((initial_node.f, initial_node))
    visited.append(initial_state)

    while len(queue) > 0:
        current_node = queue.pop(0)[1]  
        if current_node.state.isGoal():
            return current_node.getSolution()  

        for action, newGrid in current_node.state.successorFunction():
            if newGrid not in visited:
                new_state = SokobanPuzzle(newGrid)
                new_node = Node(new_state, current_node, action)
                h1 = new_node.state.h1()  
                new_node.setF(h1) 
                queue.append((new_node.f, new_node))
                visited.append(newGrid)

    return [] 


# A* avec Distance Euclidienne
def AStar2 (initial_state):
    queue=[] 
    visited = []
    initial_node=(Node(initial_state, None, None))
    initial_node.setF(0)
    queue.append((initial_node.f, initial_node))
    visited.append(initial_state)
    
    while  len(queue)>0:
        current_node = queue.pop(0)[1]
        if current_node.state.isGoal():
            return current_node.getSolution()  
        if not current_node.state.isGoal(): 
             for action, newGrid  in current_node.state.successorFunction():
                 if newGrid not in visited:
                    new_state=SokobanPuzzle(newGrid)
                    new_node = Node(new_state, current_node, action)
                    h3 = new_node.state.h3()
                    new_node.setF(h3)
                    queue.append((new_node.f, new_node))
                    visited.append(newGrid)

                    
    return []


def count_steps(result): 
    steps = 0
    print(result)
    for i in result:  
        steps += 1 
    return steps

def test_algorithm(algorithm, exemple):
    start_time = time.time()  
    puzzle = SokobanPuzzle(exemple)
    result = algorithm(puzzle)  
    end_time = time.time()    
    steps = count_steps(result)  
    return steps, end_time - start_time 


def main():

    example = [
    ['O', 'O', 'O', 'O', 'O', 'O'],
    ['O', ' ', ' ', ' ', ' ', 'O'],
    ['O', ' ', 'O', ' ', ' ', 'O'],
    ['O', 'B', ' ', 'R', ' ', 'O'],
    ['O', 'S', ' ', ' ', ' ', 'O'],
    ['O', 'O', 'O', 'O', 'O', 'O']
    ]
    
    steps_A1, time_A1 = test_algorithm(AStar, example)
    print(f"A1: Steps = {steps_A1}, Time = {time_A1:.4f} seconds")

    steps_A2, time_A2 = test_algorithm(AStar2, example)
    print(f"A2: Steps = {steps_A2}, Time = {time_A2:.4f} seconds")

    
if __name__ == "__main__":
    main()