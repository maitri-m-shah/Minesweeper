######### CLEVER ACRONYM :
######### CANNON -> Check All Neighbors of Neighbors Over Neighborhood

#### This is the advanced agent code with the additional global variable change
## The changes to this are done in the method spaceMine and the other aspects of the code are the same as in advanced.py
import numpy as np
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

#### certainMines is for values we are sure are mines (flagged or actually opened)
certainMines = []
susList = {}
 


def createmaze(d,n):
#Maitri Shah and Kajol Bhat 
    
    ## creating board where any squares that have not been visited are represented by the letter 'U'
    arr = [[0 for row in range(d)] for column in range(d)]
    listxy = []
    #print(arr)   
    
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
            
      
        #set a value to a mine
        arr[x][y] = 'M'
        listxy.append((x,y))
        count +=1
                  

    for j in range(d):
        for i in range(d):
            coordinate = ((i,j))
            mazefinder(arr,d,coordinate)

    
    return arr
    #print(arr)
    #return arr
    

## this will serve as our knowledge base
## this is a 2d array which shows what the agent knows at a given moment in time
## it starts off as all 'U's to show that all are unopened and the agent does not know whether a square is a mine or a clue
def agentmaze (arr, d):
    agent_arr = [['U' for row in range(d)] for column in range(d)]
    return agent_arr
    

## if mine, return true
def isMine (arr, x_val, y_val):
    if (arr[x_val][y_val] == 'M'):
        return True
    else:
        return False

    
### given a coordinate this finds all neighbors
### these neighbors may be opened or unopened
def neighbors(arr, d, coordinate):
    neighborList= []
#The following method is to check the neighbors of a given path
#The possible neighbors are right,left,up,down,upper right,upper left,lower right,lower,left
    x = int(coordinate[0])
    y = int(coordinate[1])
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



### for opening the first random value in the grid
def firstStep(amaze,arr,d):
    first_x = random.randint(0,d-1)
    first_y = random.randint(0,d-1)
    
    ## if random opened is already labeled as mine, skip
    while amaze[first_x][first_y] in certainMines:
        first_x = random.randint(0,d-1)
        first_y = random.randint(0,d-1) 
        
    coordinates = ((first_x,first_y))
    print("initial coordinates : ", first_x, first_y , "value:", arr[first_x][first_y])
    ## if it's a mine 
    if (isMine(arr,first_x,first_y)):
        amaze[first_x][first_y] = arr[first_x][first_y]
        openedList.append((first_x,first_y))
        

    else:
        #if the point we are on is a number
        print('alive')
        amaze[first_x][first_y] = arr[first_x][first_y]
        openedList.append((first_x,first_y))
        current = amaze[first_x][first_y]
    return coordinates


#### remove any now safe or known mine values from the suspicious list
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
    print("inside allMine")
    x = coordinates[0]
    y = coordinates[1]
    n = 0
    #if(isThereSpace(amaze,d)== False):
    #    return
    
    
    ## surrounding cells should be flagged
    for i in neighbor:
        if (amaze[i[0]][i[1]] == 'U'):
            amaze[i[0]][i[1]] = 'F'
            print("flagged")
            
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
    #print(len(coordinateList))
    #while len(coordinateList) > 90:
    #print(openedList, 'listopen')
    for i in coordinateList:
        neighbor = (neighbors(arr,d,i))
        spaceMine(amaze,arr,d,i)
        if i in openedList and kajol > 0:
            number = amaze[i[0]][i[1]]
            #print('NUMBER',number)
            #if the number is 0, the surrounding space should be 'all clear'
            if number == 0:
                mazeZeroFiller(amaze,arr,d,i,neighbor)

                #mazeRunner(amaze,arr,d,coordinates)

            if (number == len(neighbor)):
                print("number is length of neighbor")
                allMine(amaze,arr,d,i,neighbor)
            #if we accidentally opened a mine
            if number == 'M':
                MinesHit.append(i)
                cleanUpSusList()

            #if we open a spot that is not 0 or M
            elif number!= 0 and number !=8:
                mazeRunnerNeighbors(amaze,arr,d,i)
                #spaceMine(amaze,arr,d,i)
                #print(susList)
    
    ## run spaceMine to help identify safe or not twice
    ## the information that we learn from the first round of running it is then factored into the second round of running it
    for j in CompleteCoordinateList:
        spaceMine(amaze,arr,d,j)
        
    for w in CompleteCoordinateList:
        spaceMine(amaze,arr,d,w)
    
    
    
    #### 


def mazeRunnerNeighbors(amaze,arr,d,coordinates):
    #we will store all the opened elements in a list (dictionary), 
    #{1: all coordinates of 1} {2:all coordinates of 2}... until 8 
    #8 will have the least priority because we know that mines all over
    count = 0
    neighbor = (neighbors(arr,d,coordinates))
    
    
    ## for the first neighbor of the initial cell
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
            #arr
            if(amaze[i[0]][i[1]] == 0):
                mazeZeroFiller(amaze,arr,d,coordinates,neighbor) 
                spaceMine(amaze,arr,d,coordinates)
            #arr
            
           
            if(amaze[i[0]][i[1]] == '8'):
                allMine(amaze,arr,d,coordinates,neighbor)
        
            if(amaze[i[0]][i[1]] == 'M'):
                MinesHit.append((coordinates))
                spaceMine(amaze,arr,d,coordinates)
                
        
        ### for the neighbor of the neighbor of the initial cell    
        for j in neighbor2:
            spaceMine(amaze,arr,d,j)
            if (i == j):
                print('match')
            #if ((j[0],j[1]) == (i[0],i[1])):
                #susList is a list of coordinates that identify potential mines
                susList[coordinates] = None
                if coordinates in safeList:
                    safeList.remove((coordinates))
                #increment count because why not?
                count +=1
            else:
                safeList.append((j))
                #print(safeList,'HERE IS THE SAFE LIFE')
                count = 0 
                
                if (coordinates in coordinateList):
                    coordinateList.remove((coordinates))
                    
       
### if just one mine in the surrounding neighbors        
def isOneMine(amaze,arr,d,coordinates):
    
    neighbor = (neighbors(arr,d,coordinates))
    x = coordinates[0]
    y = coordinates[1]
    
    counter = 0
    for i in neighbor:
        point = amaze[i[0]][i[1]]
        if(amaze[i[0]][i[1]] == 'U'):
            return 
        
        if(amaze[i[0]][i[1]] == 'M'):
            #increment()
            return
        
        boo = isinstance(point, int)
        if(boo):
            if(amaze[i[0]][i[1]] > 0):
        #if((amaze[i[0]][i[1]]) > 1 ):
            #if all the points that are surrounding this point is 1 that would mean 
            #that this point is a mine
                counter +=1
            #N means that the agent has marked this point as a definate mine and will not go there so that 
            #it does not explode
    
    if (counter == len(neighbor)):
        certainMines.append((x,y))
        cleanUpSusList()
        if ((x,y)) in coordinateList:
            coordinateList.remove((x,y))
            #remove from sus list
            
            
#### our main method that analyzes whether mine or safe
            
def spaceMine(amaze,arr,d,coordinates):
    #point:
    x = coordinates[0]
    y = coordinates[1]
    
    uList = []
    uCounter = 0 
    mCounter = 0 #the number of mines
    neighbor = (neighbors(arr,d,coordinates))
    
    ### if all mines found using global variable, we now know everything else is safe
    if len(certainMines) == n:
        for i in range(len(amaze)):
            for j in range(len(amaze[i])):
                if amaze[i][j] == 'U':
                    amaze[i][j] = arr[i][j]
                    break
    
    ## if clue is equal to number of neighbors, they're all mines so flag all of them                
    if amaze[x][y] == len(neighbor):
        print("equals length of neighbor", amaze[x][y])
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
    
    if(mCounter + uCounter == amaze[x][y]):
        #print('you here bitch,',uList,uCounter)
        for p in uList:
            #print('ULIST VALUES BITCH,',p)
            
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
                #print('YOU ARE SO STUPID ')
                #print(amaze[x][y])
                openedList.append(([z[0]],[z[1]]))
            if ((z[0],z[1])) in susList:
                susList.remove((z[0],z[1]))
        #for s in safeNeighbors:
        #    amaze[s[0]][s[1]] = arr[s[0]][s[1]]
        #    if(arr[s[0]][s[1]] == 'M'):
        #        print('YOU ARE SO STUPID 2 ',len(uList))
        #    openedList.append(([s[0]],[s[1]]))
        #    if ((s[0],s[1])) in susList:
        #        susList.remove((s[0],s[1]))
            

          
## if we visit a clue that is 0, this recursively fills all zeroes's neighbors in as all of these cells will be safe
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
                
    
             

## checks if unopened cells near
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
    
    
def MazeAgentSolving(amaze, maze, d):
    for i in coordinateList:
        while((amaze[i[0]][i[1]] == 'U')):
            mazeSolver(amaze, maze, d)

            
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
amaze = agentmaze(maze, d)
#mazeSolver(amaze, maze, d)
MazeAgentSolving(amaze, maze, d)
for row in amaze:
    print(" ".join(str(cell) for cell in row))
    
    
    
print("""""")
for row in maze:
    print(" ".join(str(cell) for cell in row))
    
print_score(d, amaze)
