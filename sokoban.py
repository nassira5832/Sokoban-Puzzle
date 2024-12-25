import math
import time 
import heapq  
from itertools import count 
from heapq import heappush, heappop

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
                    newGrid[x][y]= 'S' if self.grid[x][y] == '.' else ' ' 
                    newGrid[newX][newY]='.'
                    successors.append((i, newGrid))

                if (self.grid[newX][newY]==' '):
                    newGrid = [row[:] for row in self.grid]
                    newGrid[x][y]= 'S' if self.grid[x][y] == '.' else ' ' 
                    newGrid[newX][newY]='R'
                    successors.append((i, newGrid))

                if(self.grid[newX][newY]=='B' ):
                    if (0 <= newX+dx < len(self.grid) and 0 <= newY+dy< len(self.grid[0]) and self.grid[newX+dx][newY+dy]!='O' and self.grid[newX+dx][newY+dy]!='*'and self.grid[newX+dx][newY+dy]!='B'):
                     
                        if(self.grid[newX+dx][newY+dy]==' '):
                           newGrid = [row[:] for row in self.grid]
                           newGrid[x][y]= 'S' if self.grid[x][y] == '.' else ' '  
                           newGrid[newX][newY]='R'
                           newGrid[newX+dx][newY+dy]='B'
                           successors.append((i, newGrid))

                        if(self.grid[newX+dx][newY+dy]=='S'):
                            newGrid = [row[:] for row in self.grid]
                            newGrid[x][y]= 'S' if self.grid[x][y] == '.' else ' ' 
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
    def h3(self):
        manhattan_sum = 0
        dist = []
        min_player_to_box =0
        for box in self.boxes:
           distance = self.manhattan_distance(self.player, box)
           dist.append(distance)  
        print("Distances from player to boxes:", dist)
        for box in self.boxes:
            distances = [self.manhattan_distance(box, target) for target in self.target]
            if distances:
              min_distance = min(distances)
              manhattan_sum += min_distance
        if dist==[]:
            min_player_to_box =2
        else: 
            min_player_to_box = min(dist)
        return min_player_to_box + manhattan_sum 
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
    

def BFS(initial_state):
    queue = [] 
    visited = set() 
    initial_node = Node(initial_state, None, None) 

    if initial_node.state.isGoal():  
        return initial_node.getSolution()

    queue.append(initial_node) 
    visited.add(tuple(tuple(row) for row in initial_state.grid)) 
    while len(queue) > 0:  
        current_node = queue.pop(0)  
        visited.add(tuple(tuple(row) for row in current_node.state.grid))  

        for action, newGrid in current_node.state.successorFunction(): 
            new_state = SokobanPuzzle(newGrid) 

            new_state_tuple = tuple(tuple(row) for row in new_state.grid) 
            if new_state_tuple not in visited and new_state_tuple not in (tuple(tuple(row) for row in n.state.grid) for n in queue):  
                child_node = Node(new_state, current_node, action) 
                if child_node.state.isGoal(): 
                    return child_node.getSolution()
                queue.append(child_node) 

    return [] 

import heapq
from itertools import count

def is_corner_deadlock(grid, box_position):
    """Check if a box is in a corner deadlock position""" 
    x, y = box_position
    if grid[x][y] == 'B':  # Vérifier si la position contient un bloc
        # Vérification des coins
        if (x - 1 >= 0 and grid[x - 1][y] == 'O' and y - 1 >= 0 and grid[x][y - 1] == 'O') or \
           (x + 1 < len(grid) and grid[x + 1][y] == 'O' and y + 1 < len(grid[0]) and grid[x][y + 1] == 'O'):
            return True
    return False

def is_line_deadlock(grid, box_position):
    """Check if a box is in a line deadlock position""" 
    x, y = box_position
    if grid[x][y] == 'B':  # Vérifier si la position contient un bloc
        # Vérification des lignes
        if (x - 1 >= 0 and grid[x - 1][y] == 'B' and x + 1 < len(grid) and grid[x + 1][y] == 'O') or \
           (y - 1 >= 0 and grid[x][y - 1] == 'B' and y + 1 < len(grid[0]) and grid[x][y + 1] == 'O'):
            return True
    return False

def contains_deadlock(grid):
    """Check the entire grid for any deadlock conditions."""
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == 'B': 
                if is_corner_deadlock(grid, (x, y)) or is_line_deadlock(grid, (x, y)):
                    return True
    return False

def AStar(initial_state, heuristic='h3'):
    queue = [] 
    visited = set()  
    counter = count()  

    initial_node = Node(initial_state, None, None)
    h_value = initial_node.state.h3()
    initial_node.setF(h_value) 
    heapq.heappush(queue, (initial_node.f, next(counter), initial_node))  

    visited.add(tuple(tuple(row) for row in initial_state.grid))

    while queue:
        current_node = heapq.heappop(queue)[2] 
        
        if current_node.state.isGoal():  
            return current_node.getSolution() 

        for action, newGrid in current_node.state.successorFunction():
            newGrid_tuple = tuple(tuple(row) for row in newGrid)  
            if not contains_deadlock(newGrid) and newGrid_tuple not in visited:  
                new_state = SokobanPuzzle(newGrid)
                new_node = Node(new_state, current_node, action)
                h_value = new_node.state.h3()  
                new_node.setF(new_node.g + h_value)  
                heapq.heappush(queue, (new_node.f, next(counter), new_node)) 
                visited.add(newGrid_tuple)  

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
    if algorithm==BFS :
        result = algorithm(puzzle,) 
    else: 
        result = algorithm(puzzle,'h1') 
    end_time = time.time()    
    steps = count_steps(result)  
    return steps, end_time - start_time 


def main():

    example= [
    ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ['O', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'O'],
    ['O', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'O'],
    ['O', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'O'],
    ['O', ' ', ' ', ' ', 'O', 'O', 'O', ' ', ' ', 'O'],
    ['O', ' ', ' ', ' ', ' ', ' ', 'O', '.', ' ', 'O'],
    ['O', ' ', ' ', ' ', ' ', ' ', ' ', 'O', ' ', 'O'],
    ['O', ' ', ' ', ' ', 'B', ' ', ' ', 'O', ' ', 'O'],
    ['O', ' ', ' ', ' ', ' ', ' ', ' ', 'O', ' ', 'O'],
    ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']  
    ]
   

    steps_A1, time_A1 = test_algorithm(AStar, example)
    print(f"A1: Steps = {steps_A1}, Time = {time_A1:.4f} seconds")


    steps_bfs, time_bfs = test_algorithm(BFS, example)
    print(f"BFS: Steps = {steps_bfs}, Time = {time_bfs:.4f} seconds")

if __name__ == "__main__":
    main()