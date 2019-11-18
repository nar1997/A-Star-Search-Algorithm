from MazeTools import Maze
from MazeTools import getMazeList
import os 
import pickle
import timeit
import copy
from statistics import median, mean

from FHeap import FHeap
from MazeTools import Action


openList = None
closed = None

counter = 0
search = {}

tree = {}
knownBlockages = []
fullPathList = []

maze = None 

def aStar(start, goal, adaptive=False):
    global maze, openList, closed, search, counter, tree, knownBlockages
    
    expandedNodes = 0
    
    while ('g' not in maze.get(goal).__dict__ or maze.get(goal).g > openList.getMin().f):
        try:    
            s = openList.delMin().coord
        except: # this occurs if goal was never reached 
            return expandedNodes # first while condition will allow it to run but all routes were dead end
        
        expandedNodes += 1
        closed.append(s) 
        
        for a in Action:
            succ = maze.getSucc(s, a)
            
            if succ == None: # successor is in a wall or some shit
                continue 
            
            if succ not in search or search[succ] < counter:
                try:
                    maze.get(succ).__dict__.pop('g') # delete the associated g value
                except:
                    pass 
                
                search[succ] = counter
                
            condition = True
            
            if (succ in knownBlockages): # cost to get here is inf
                condition = False
            elif ('g' not in maze.get(succ).__dict__): # g is inf
                condition = True 
            elif (maze.get(succ).g <= maze.get(s).g + 1):
                condition = False
                
            if (condition):
                maze.get(succ).g = maze.get(s).g + 1

                tree[maze.get(succ)] = maze.get(s)
                
                openList.deleteState(maze.get(succ))
                maze.get(succ).f = computeF(succ, goal)
                openList.insert(maze.get(succ))
    
    if adaptive == True:
        goalDistance = maze.get(goal).g
        
        for coord in closed:
            state = maze.get(coord)
            state.h = goalDistance - state.g
    
    return expandedNodes        
    
def repeatedBackAStar(mazeObj, start, goal, adaptive=False):
    return repeatedAStar(mazeObj, goal, start, adaptive)
                
def repeatedAStar(mazeObj, start, goal, adaptive=False):
    global maze, counter, search, openList, closed, knownBlockages, tree, fullPathList
    
    maze = mazeObj
    counter = 0
    search = {}
    tree = {}
    knownBlockages = []
    fullPathList = []
    expandedNodes = 0
    
    while (start != goal):
        counter += 1
        
        #print('Counter: {0}, Start: {1}'.format(counter, start))
        #print(maze.toString(fullPathList))
        
        addBlockages(start)
        
        maze.get(start).g = 0
        search[start] = counter
        
        try:
            maze.get(goal).__dict__.pop('g') # delete the associated g value (effectively set it to inf)
        except:
            pass 
        
        openList = FHeap()
        closed = []
        
        maze.get(start).f = computeF(start, goal)
        openList.insert(maze.get(start))
        
        expandedNodes += aStar(start, goal, adaptive)
        
        if openList.isEmpty():
            print(maze.toString(fullPathList))
            print("unsolvable")
            return expandedNodes 
        
        start = followPath(start, goal).coord
        
        print('{0}Counter: {1}'.format(maze.toString(fullPathList), counter))
    
    return expandedNodes
        
    

def followPath(start, goal): 
    global maze, tree, knownBlockages, fullPathList
 
    pathList = getPathList(start, goal)
    
    currState = pathList[0]
    
    for i in range(1, len(pathList)):
        next = pathList[i]
        
        if (next.blocked == 1):
            knownBlockages.append(next.coord)
            
            while True:
                try:
                    pathList.pop(i) # cut off rest of path (unreachable)
                except:
                    break 
            
            break
        
        currState = next 
        
    if len(fullPathList) != 0:
        pathList.pop(0)
        
    fullPathList += pathList     
    return currState

def addBlockages(start):
    global maze
    
    for a in Action:
        succ = maze.getSucc(start, a)
        
        if succ == None:
            continue
        
        succState = maze.get(succ) 
        
        if succState.blocked == 1:
            if succ not in knownBlockages:
                knownBlockages.append(succ)
        

def getPathList(start, goal):
    global tree
    
    t = maze.get(goal)
    
    pathList = []

    while True:        
        pathList.insert(0, t)
        
        try:
            t = tree[t]
        except:
            return pathList  
        
        if t.coord == start:
            pathList.insert(0, t)
            return pathList
    
def printTree(start, goal):
    global tree, maze
    t = maze.get(goal)
    
    pathList = []

    while True:        
        pathList.append(t)
        
        try:
            t = tree[t]
        except:
            break    

    print(maze.toString(pathList))
    
def computeF(tupe, goal):
    global maze 
     
    g = maze.get(tupe).g
    
    try: 
        h = maze.get(tupe).__dict__['h'] # for adaptive astar
    except:
        h = heur(tupe, goal)
        
    return g + h
        
def heur(start, goal):
    return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

def main():
    NUM_MAZES = 5
    SIZE_MAZE = 50
    
#    mazeList = getMazeList(NUM_MAZES, SIZE_MAZE)
    runtime = [[0 for j in range(NUM_MAZES)] for i in range(2)]
    counter = [[0 for j in range(NUM_MAZES)] for i in range(2)]
    
    for i in range(NUM_MAZES):
        m = Maze(SIZE_MAZE)
        
        numExpanded = repeatedAStar(m, m.start, m.goal) # forwardA
        
    return 


    
    # FORWARD repeatedAStar(m, m.start, m.goal)
    # ADAPTIVE FORWARD: repeatedAStar(m, m.start, m.goal, True)
    # BACKWARD repeatedBackAStar(m, m.start, m.goal) 
    for i in range(NUM_MAZES):
        path = 'mazes/maze{0}.dat'.format(i)
 
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
         
        with open(path, 'rb') as f:
            m = pickle.load(f)
        
        m = Maze(SIZE_MAZE)
        
        startTime = timeit.default_timer()
        counter[0][i] = repeatedAStar(m, m.start, m.goal)
        stopTime = timeit.default_timer()
        runtime[0][i] = 1000 * (stopTime - startTime) 
          
        m.reset()
            
        startTime = timeit.default_timer()
        counter[1][i] = repeatedAStar(m, m.start, m.goal, True)
        stopTime = timeit.default_timer()
        runtime[1][i] = 1000 * (stopTime - startTime) 
          
        print('Maze {0} complete...'.format(i+1))
#         print()
#         print('Start: {0}'.format(m.start))
#         print('Goal: {0}'.format(m.goal))
#         print('Runtime (ForwardA): {0:.0f} ms'.format(forwardATime))
#         print('Runtime (ForwardAdapt): {0:.0f} ms'.format(forwardAAdaptTime))
#         print("/" * (int) (SIZE_MAZE * 1.05))
#         print()
       
    avgRun0 = mean(runtime[0])
    avgRun1 = mean(runtime[1])
    avgCount0 = mean(counter[0])
    avgCount1 = mean(counter[1])
      
    medRun0 = median(runtime[0])
    medRun1 = median(runtime[1])
    medCount0 = median(counter[0])
    medCount1 = median(counter[1])
       
    print('{0} Mazes - {1}x{1}'.format(NUM_MAZES, SIZE_MAZE))
    print('Backward-Forward:')
    print('Nodes expanded (average):\t{0:.1f} - {1:.1f} = {2:.1f}'.format(avgCount1, avgCount0, avgCount1-avgCount0))
    print('Nodes expanded (median):\t{0:.1f} - {1:.1f} = {2:.1f}'.format(medCount1, medCount0, medCount1-medCount0))
    print('Runtime (ms) (average):\t{0:.1f} - {1:.1f} = {2:.1f}'.format(avgRun1, avgRun0, avgRun1-avgRun0))
    print('Runtime (ms) (median):\t{0:.1f} - {1:.1f} = {2:.1f}'.format(medRun1, medRun0, medRun1-medRun0))
  
if __name__=="__main__":
    main()



