import random
from enum import Enum

class State:
    def __init__(self, coord, **kwargs):
        self.coord = coord
        self.blocked = 0
        self.__dict__.update(kwargs)
        
    def __str__(self):
        return self.__dict__.__str__()
    
    def __lt__(self, other):
        try:
            fself = self.f
            fother = other.f
            
            if fself < fother:
                return True
            if fself > fother:
                return False
        except:
            pass
        
        try:
            gself = self.g
            gother = other.g
            
            if gself > gother: # we want the > g to go first in the minheap
                return True  # so need the higher gvalue State to be < the other one
            if gself < gother:
                return False
        except:
            pass
        
        return 0 == random.randrange(2)
         

    
class Action(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

class Maze:
    def __init__(self, size):
        self.size = size
        self.start = None
        self.goal = None
        
                
        self.maze = self.generateMaze()
        
        self.__setStartAndGoal__()

        
    def __str__(self):
        return self.toString()   
    
    def reset(self):
        for i in range(self.size):
            for j in range(self.size):
                if 'g' in self.get((i,j)).__dict__:
                    self.get((i,j)).__dict__.pop('g')
                if 'h' in self.get((i,j)).__dict__:
                    self.get((i,j)).__dict__.pop('h')            
                if 'f' in self.get((i,j)).__dict__:
                    self.get((i,j)).__dict__.pop('f')                
    
        return self
    
    def toString(self, pathList = None):
        s = ''  
        
        s += '+' * (self.size + 2)
        s += '\n'
        
        
        for i in range(self.size):
            s += '+'
            
            for j in range(self.size):
                if (i,j) == self.start:
                    s += "S"
                elif (i,j) == self.goal:
                    s += "G"
                elif self.maze[i][j].blocked == 1:
                    s += '+'
                elif pathList != None and self.get((i,j)) in pathList:
                        s += 'O'
                else:
                    s += ' '
    
            s += '+ {0}\n'.format(i)

        s += '+' * (self.size + 2)
        
        s += '\n '
        
        if (self.size > 10):
            for i in range((int) ((self.size - 1)/10) + 1):
                s += '{0}'.format(i)
                s += ' ' * 9
            
            s += '\n '
        
        for i in range(self.size):
            s += '{0}'.format(i%10)
        
        s += '\n'    
        
        return s  
    
    def get(self, coord):
        return self.maze[coord[0]][coord[1]]
    
    def getSucc(self, tupe, action):
        x = 0 if (action == Action.NORTH or action == Action.SOUTH) else 1 if action == Action.EAST else -1
        y = 0 if (action == Action.EAST or action == Action.WEST) else -1 if action == Action.NORTH else 1 
    
        newTuple = (tupe[0] + y, tupe[1] + x) 
        
        if self.isInBounds(newTuple):
            return newTuple
        
        return None
        
    def isInBounds(self, tupe):
        x = tupe[0]
        y = tupe[1]
        
        if x >= self.size or x < 0:
            return False
        
        if y >= self.size or y < 0:
            return False
        
        return True
    
    def generateMaze(self):
        maze = [[State((i,j)) for j in range(self.size)] for i in range(self.size)]
        
        x = random.randrange(self.size)
        y = random.randrange(self.size)
        
        tupe = (x, y)
        
        visited = [tupe]
        stack = [tupe]
        
        while len(visited) < self.size*self.size:
            while True:
                tupe = self.__getRandomSucc__(tupe, visited)
                
                if (tupe == None): # no successor
                    if len(stack) == 0:
                        tupe = self.__getUnvisited__(visited)
                        break
                    
                    tupe = stack.pop()
                else:
                    break
              
            visited.append(tupe)
            stack.append(tupe)
    
            maze[tupe[0]][tupe[1]].blocked = 1 if random.randrange(100) < 30 else 0
        
        return maze    
    
    def __setStartAndGoal__(self):
        while True:
            startTuple = (random.randrange(self.size), random.randrange(self.size))
            
            if self.get(startTuple).blocked == 0:
                self.start = startTuple
                break
        
        while True:
            goalTuple = (random.randrange(self.size), random.randrange(self.size))
            
            if goalTuple != startTuple and self.get(goalTuple).blocked == 0:
                self.goal = goalTuple 
                break       
        
    def __getRandomSucc__(self, tupe, visited):
        actions = [Action.NORTH, Action.EAST, Action.SOUTH, Action.WEST]
        random.shuffle(actions)
        
        for a in actions:
            succ = self.getSucc(tupe, a) 
            
            if succ != None and succ not in visited:
                return succ
            
        return None
    
    def __getUnvisited__(self, visited):
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) not in visited:
                    return (i, j)
                
        return None  

def getMazeList(numMazes, size):
    list = []
    
    for i in range(numMazes):
        list.append(Maze(size))
        
    return list

def main():
    pass
    s1 = State((0,0))
    print(State((0,0),g=4,h=5,f=5).__sizeof__())
    s1.g=4
    s1.f=5
    s1.h=8
    print(s1.__sizeof__())
    print(s1)
#     s2 = State((0,0))
#     
#     s1.f = 94
#     s2.f = 94
#     
#     s1.g = 88
#     s2.g = 88
#     
#     #print (s1==s2)
#     print (s1<s2)
    
#     for m in getMazeList(1, 23):
#         #print(m)
#         
#         state = m.get((0,0))
#         
#         print (state)
#         
#         state.test = 69
#         
#         print (state)
#         
#         print (state.__dict__)
#         
#         state.g = 4 
#         
#         print(state.__dict__)
#         
#         state.__dict__.pop('g')
#     
#         print(state.__dict__)

if __name__=="__main__":
    main()



