######### CLEVER ACRONYM :
######### SCAN -> Single Cell Analyze Neighbors
import numpy as np
import math as math
import random
import sys
sys.setrecursionlimit(1500)

res = []
safeList = []
openedList = []
MinesHit = []

d = int(input("Enter the dimensions of maze")) 
n = int(input("Enter the number of mines"))
#The coordinate list holds every single sqaure on the game. 
#As we play the game, we will move coordinates to the mines list and safe list
#until this list is empty

coordinateList = []
for i in range(d):
    for j in range(d):
        coordinateList.append((i,j))
        
CompleteCoordinateList = []
for i in range(d):
    for j in range(d):
        CompleteCoordinateList.append((i,j))

certainMines = []
susList = {}
 


def createmaze(d,n):
#Maitri Shah and Kajol Bhat 
    
    ## creating board where any squares that have not been visited are represented by the letter 'U'
    arr = [[0 for row in range(d)] for column in range(d)]
    listxy = [] 
    
    #count returns how many mines there are 
    count = 0 
    # to add mines
    for k in range(n):
        x = random.randint(0,d-1)
        #print(x)
        y = random.randint(0,d-1)
        
        #to make sure that we go to a new point every time
        while (x,y) in listxy:
            x = random.randint(0,d-1)
            y = random.randint(0,d-1)
            
      
        #set a value to a bomb
        arr[x][y] = 'M'
        listxy.append((x,y))
        count +=1
                  
    ### so we can go through all coordinates when we run the rest of program
    for j in range(d):
        for i in range(d):
            coordinate = ((i,j))
            mazefinder(arr,d,coordinate)

    
    return arr
    

## agent maze represents all the knowledge that the agent has
def agentmaze (arr, d):
    agent_arr = [['U' for row in range(d)] for column in range(d)]
    return agent_arr
    

## True if mine, False if not
def isMine (arr, x_val, y_val):
    if (arr[x_val][y_val] == 'M'):
        return True
    else:
        return False
    
def neighbors(arr, d, coordinate):
    neighborList= []
#The following method is to check the neighbors of a given path
#The possible neighbors are right,left,up,down,upper right,upper left,lower right,lower,left
    x = int(coordinate[0])
    #print(x)
    y = int(coordinate[1])
    #print(y)
    counter = int(0)


    if ((x+1 < d and ((y)<d))):
        neighborList.append((x+1,y))
        

    if ((x-1>=0 and y<d)):
        neighborList.append((x-1,y))

    if ((x<d) and (y+1)<d):
        neighborList.append((x,y+1))

    if ((x < d) and (y-1)>=0):
        neighborList.append((x,y-1))
            
    if ((x+1 <d and (y+1)<d)):
        neighborList.append((x+1,y+1))
            
    if ((x+1 <d) and (y-1) >=0):
        neighborList.append((x+1,y-1))


    if ((x-1 >=0 and (y+1) <d)):
        neighborList.append((x-1,y+1))
            
    if ((x-1 >=0) and (y-1) >=0):
        neighborList.append((x-1,y-1))

    return neighborList


## chooses point at random to open as the first opened cell
def firstStep(amaze,arr,d):
    first_x = random.randint(0,d-1)
    first_y = random.randint(0,d-1)
    
    
    while amaze[first_x][first_y] in certainMines:
        first_x = random.randint(0,d-1)
        first_y = random.randint(0,d-1)  
   
    coordinates = ((first_x,first_y))
    #print("initial coordinates : ", first_x, first_y , "value:", arr[first_x][first_y])
    
    ## if mine, open it and label as 'M' in agent maze
    if (isMine(arr,first_x,first_y)):
        amaze[first_x][first_y] = arr[first_x][first_y]
        openedList.append((first_x,first_y))
        

    else:
        #if the point we are on is a number
        amaze[first_x][first_y] = arr[first_x][first_y]
        openedList.append((first_x,first_y))
        current = amaze[first_x][first_y]
    return coordinates


## remove values that we are certain are mines from 'suspicious list'
def cleanUpSusList():
    tempList = []
    for i in susList.keys():
        for j in certainMines:
            if (i == j):
                tempList.append(i)
    for t in tempList:
        if t in susList.keys():
            del susList[t]

#Task: 


### if we know that every value around a cell is a mine
### ex : if the clue is 8
def allMine(amaze,arr,d,coordinates,neighbor):
    #print("inside allMine")
    x = coordinates[0]
    y = coordinates[1]
    n = 0

    
    for i in neighbor:
        if (amaze[i[0]][i[1]] == 'U'):
            amaze[i[0]][i[1]] = 'F'
            #print("flagged")
            
            if (i[0],i[1]) in coordinateList:
                coordinateList.remove((i[0],i[1]))
                openedList.append((i[0],i[1]))
                
            if(arr[i[0]][i[1]] == len(neighbor)):
                 amaze[i[0]][i[1]] = 'F' 
    
    
def mazeSolver(amaze, arr, d):
    kajol = 0 
    neighborsdict=dict()
    #first step
    #finding the coordinates of the random point selected
    coordinates = firstStep(amaze,arr,d)
    #check the neighbors of the first step taken, find out what is safe
    mazeRunnerNeighbors(amaze,arr,d,coordinates)
    kajol += 1
    #number represents the mines that are neighboring the point randomly selected
    #number = arr[coordinates[0]][coordinates[1]]

        #(d*d - (len(coordinateList))) >= 0 


    for i in coordinateList:
        neighbor = (neighbors(arr,d,i))
        spaceMine(amaze,arr,d,i)
        if i in openedList and kajol > 0:
            number = amaze[i[0]][i[1]]
            #if the number is 0, the surrounding space should be 'all clear'
            if number == 0:
                mazeZeroFiller(amaze,arr,d,i,neighbor)

                #mazeRunner(amaze,arr,d,coordinates)

            if (number == len(neighbor)):
                #print("number is length of neighbor")
                allMine(amaze,arr,d,i,neighbor)
            #if we accidentally opened a mine
            if number == 'M':
                MinesHit.append(i)
                cleanUpSusList()

            #if we open a spot that is not 0 or M
            elif number!= 0 and number !=8:
                mazeRunnerNeighbors(amaze,arr,d,i)
                #spaceMine(amaze,arr,d,i)
                #print('HERE IS THE SUS LIST')
                #print(susList)
    
    ## run it twice so it can take information learned in first run, and incorporate into second run
    ## additional information learned and factored
    for j in CompleteCoordinateList:
        spaceMine(amaze,arr,d,j)
        
    for w in CompleteCoordinateList:
        spaceMine(amaze,arr,d,w)



def mazeRunnerNeighbors(amaze,arr,d,coordinates):
    #we will store all the opened elements in a list (dictionary), 
    #{1: all coordinates of 1} {2:all coordinates of 2}... until 8 
    #8 will have the least proirity because we know that mines all over
    count = 0
    neighbor = (neighbors(arr,d,coordinates))

    
    ## in basic agent, unlike advanced we only check the neighbors of one cell at a time
    
    for i in neighbor:
        if (count == 0):
            #print('count',count)
            count += 1
            coordinates = ((i[0],i[1]))
            neighbor2 = (neighbors(arr,d,coordinates))
            if (amaze[i[0]][i[1]] != 'F'):
                amaze[i[0]][i[1]] = arr[i[0]][i[1]]
            openedList.append((i[0],i[1]))
            if ((i[0],i[1])) in susList:
                susList.remove((i[0],i[1]))
            
            if (coordinates in coordinateList):
                coordinateList.remove((coordinates))

            if(amaze[i[0]][i[1]] == 0):
                mazeZeroFiller(amaze,arr,d,coordinates,neighbor) 
                spaceMine(amaze,arr,d,coordinates)
            
           
            if(amaze[i[0]][i[1]] == '8'):
                allMine(amaze,arr,d,coordinates,neighbor)
        
            if(amaze[i[0]][i[1]] == 'M'):
                MinesHit.append((coordinates))
                spaceMine(amaze,arr,d,coordinates)

                
## main method where we use inference to determined whether to flag something as a mine or determine if safe
def spaceMine(amaze,arr,d,coordinates):
    #point:
    x = coordinates[0]
    y = coordinates[1]
    
    uList = []
    uCounter = 0 
    mCounter = 0 #the number of mines
    neighbor = (neighbors(arr,d,coordinates))
    
    ## if clue is equal to number of neighbors, they're all mines so flag all of them                
    if amaze[x][y] == len(neighbor):
        #print("equals length of neighbor", amaze[x][y])
        for z in neighbor:
            if (amaze[z[0]][z[1]] == 'U'):
                amaze[z[0]][z[1]] = 'F'
                print("added an F to neighbor line 375")
    safeNeighbors = [] #all or none
    for i in neighbor:
    #go through all the neighbors of point
    #neighbor(lenght)-number(point)
        safeNeighbors.append(i)
        
        
        if amaze[i[0]][i[1]] == 'U':
            uCounter += 1
            uList.append(i)
        if (amaze[i[0]][i[1]] == 'M') or (amaze[i[0]][i[1]] == 'F') :
            mCounter += 1
            
    ## all 'U' cells are mines
    if(mCounter + uCounter == amaze[x][y]):
 
        for p in uList:
            
            if p not in certainMines:
                amaze[p[0]][p[1]] = 'F'
                certainMines.append(p)
                uList.remove(p)
                if (coordinates in coordinateList):
                    coordinateList.remove((coordinates))
                if (coordinates in safeList):
                    safeList.remove((coordinates))
    for p in uList:                 
        if p in certainMines:
            if p in uList:
                uList.remove(p)
            #print('ADDED A SPACE MINE')
     
    #### if all u values safe
    if (mCounter == amaze[x][y]):
        #clear the umaze
        for z in uList:
            if (amaze[z[0]][z[1]] != 'F'):
                amaze[z[0]][z[1]] = arr[z[0]][z[1]]
            if(arr[z[0]][z[1]] == 'M'):
                #print(amaze[x][y])
                openedList.append(([z[0]],[z[1]]))
            if ((z[0],z[1])) in susList:
                susList.remove((z[0],z[1]))

            

            
### if we open a zero clue, we recursively open all surrounding cells if there are more zeroes
## anything neighboring zero is definately safe
def mazeZeroFiller(amaze,arr,d,coordinates,neighbor):
    x = coordinates[0]
    y = coordinates[1]
    n = 0
    
    if(isThereSpace(amaze,d)== False):
        return
    
    for i in neighbor:
        if (amaze[i[0]][i[1]] == 'U'):
            amaze[i[0]][i[1]] = arr[i[0]][i[1]]
            
            if (i[0],i[1]) in coordinateList:
                coordinateList.remove((i[0],i[1]))
                openedList.append((i[0],i[1]))
                
            if(arr[i[0]][i[1]] == 0 ):
                mazeZeroFiller(amaze,arr,d,i,neighbors(arr, d, i))
                
    
             
## are there unopened cells to check
def isThereSpace(amaze,d):
    n = 0
    for n in range(d):
        if 'U' in amaze[n]:
            return True
        else:
            return False
        
        
    
def mazefinder(arr, d, coordinate):
#The following method is to check the neighbors of a given path
#The possible neighbors are right,left,up,down,upper right,upper left,lower right,lower,left
    #print("coordinate = ", coordinate)
    x = int(coordinate[0])
    #print(x)
    y = int(coordinate[1])
    #print(y)
    minecounter = 0
    notminecounter = 0
    neighborList = neighbors(arr, d, coordinate)
    
    if (arr[x][y] == 'M'):
        return
 
    for p in neighborList:
        if (arr[p[0]][p[1]] == 'M'):
            arr[p[0]][p[1]] = 'M'
            minecounter += 1
        if(arr[p[0]][p[1]] != 'M'):
            notminecounter += 1
    
    arr[coordinate[0]][coordinate[1]] = minecounter
            

    return
#Runs until there are no many Unopened spots
    

## call solver
def MazeAgentSolving(amaze, maze, d):
    for i in coordinateList:
        while((amaze[i[0]][i[1]] == 'U')):
            mazeSolver(amaze, maze, d)


            
## print final score
def print_score(d, amaze):    
    mine_count_val = 0
    f_count_val = 0
    print("""""")   
    for r in range(d):
        for c in range(d):
            if amaze[r][c] == 'M':
                mine_count_val +=1
                
            if amaze[r][c] == 'F':
                f_count_val +=1
                
    print('mines hit,', mine_count_val)
    print('mines avoided,', f_count_val)
    final_score = float(f_count_val / (n))
    final_score = final_score*100
    print("Final Score = ", final_score,'%')
    
    
maze = createmaze(d,n)
#print(maze)
amaze = agentmaze(maze, d)
#mazeSolver(amaze, maze, d)
MazeAgentSolving(amaze, maze, d)
for row in amaze:
    print(" ".join(str(cell) for cell in row))
    
    
    
print("""""")
for row in maze:
    print(" ".join(str(cell) for cell in row))
    
print_score(d, amaze)
