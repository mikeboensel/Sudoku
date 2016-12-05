'''
Created on Dec 4, 2016

@author: User
'''

if __name__ == '__main__':
    pass

board = []
cellPossibilities = {} #hashMap for position sets (possible values a cell can take)

#useful in combo with the findNeighborRange() to get all box members
cellFromEachBox = [(0,0), (0,4), (0,8), (4,0), (4,4), (4,8), (8,0), (8,4), (8,8)]    

totalSolved = 0

'''Only allowable dupe is the _ (unknown cell value) character
'''
def hasDupe(myList):
    s= set()
    for listItem in myList:
        if listItem in s and listItem != '_':
            return True
        s.add(listItem)
    return False
    
def checkPositionRange(pos, msg):
    if pos > 8 or pos < 0:
        print("Bad input " + pos + " " + msg)
        exit

'''Pass in the y you are interested in 
'''
def getRow(y):
    return board[y]
    
'''Pass in the x you are interested in 
'''
def getCol(x):
    checkPositionRange(x, "From getCol")
    col = []
    for y in range(0,9):
        col.append(getRow(y)[x])
        
    return col

def getPosition(x,y):
    row = getRow(y)
    return row[x]
    
def findNeighborsRanges (a):
    if a <= 2:
        return [0,1,2]
    elif a <=5:
        return [3,4,5]
    elif a <=8:
        return [6,7,8]
    return None
    
def getBoxNeighbors(x, y):
    boxMembers = getBoxNeighborCoordList(x, y)
    
    box = []
    for member in boxMembers:
        box.append(getPosition(member[0], member[1]))
    return box

def getBoxNeighborCoordList(x,y):
    checkPositionRange(x, "GetBox x")
    checkPositionRange(y, "GetBox y")
    
    xRange = findNeighborsRanges(x)    
    yRange = findNeighborsRanges(y)

    return [(x,y) for x in xRange for y in yRange]

def printNeighborsAsBox(x,y):
    neighbors = getBoxNeighbors(x, y)
    out = ''
    for i in range(9):
        out += neighbors[i] + ' '
        if i == 2 or i == 5:
            print(out)
            out = ''
    print(out)
    
'''Print row by row, with standard box looking format (pipes (|) and minuses (-))
'''
def printBoard():
    global totalSolved
    totalSolved +=1

    print("{} cells solved:".format(totalSolved))
    
    out = ''
    for y in range(9): #for reach row
        if y == 3 or y == 6:
            print('----------------------')
        row = getRow(y)
        for x in range(9): # print a nice spaced, | delimited output
            if x == 3 or x == 6:
                out += '| '
            out+=row[x]
            out+= ' '
            
        print(out)
        out = ''
        
    print("\n\n")
        
def isvalidBoard():
    for i in range(9):
        if hasDupe(getRow(i)):
            return False
        if hasDupe(getCol(i)):
            return False
        
    for cell in cellFromEachBox:
        if hasDupe(getBoxNeighbors(cell[0], cell[1])):
            return False

    return True
        
def guardedAppend(tripletSize, expectedPipePosition, currRow, prevCharWasPipe):
    l = len(currRow)
    
    if l == expectedPipePosition and prevCharWasPipe == False:
        pass  # pipe in expected delimiting position (for a full triplet). No expansion of row representation required
    else: 
        while len(currRow) < tripletSize:
            # Shortcut conditions appear next (meaning skipped a bunch of underscores for notational ease)
            currRow.append("_")

'''@returns set with 1-9 (inclusive) values
'''
def build1To9Set():
    s = set()
    for i in range(1,10):
        s.add(i)
    return s

'''Takes a key k, map m, and value.
Check if the k is in the map. If so is the value in the set (the map's value). If so remove value from set.
'''
def pythonBoilerplate(k, m, val):
    if k in m:
        if val in m[k]:
            m[k].remove(val)
            if len(m[k]) == 1:
                updateUnknownCell(k[0], k[1], (list(m[k])[0]))

def updateDependentPossibilities(x, y, val):
    for t in range(9):
        pythonBoilerplate((x,t), cellPossibilities, val)
        pythonBoilerplate((t,y), cellPossibilities, val)
        
#         if (x,t) in cellPossibilities:
#             cellPossibilities[(x,t)].remove(val)
#         if (t,y) in cellPossibilities:
#             cellPossibilities[(t,y)].remove(val)
        
    for n in getBoxNeighborCoordList(x, y):
        pythonBoilerplate(n, cellPossibilities, val)
#         if n in cellPossibilities:
#             if val in cellPossibilities[n]:
#                 cellPossibilities[n].remove(val)    
        


def updateUnknownCell(x, y, val):
    existingVal = getPosition(x, y)
    if existingVal != '_':
        print("Bad attempt to update cell ({},{} ), tried to overwrite existing {} with {}".format(x,y,existingVal, val))
        exit
    board[y][x] = val
    
    printBoard()
    
    if isvalidBoard() == False:
        print("Broke at this point ")
        print(cellPossibilities)
            
    if (x,y) in cellPossibilities:
        cellPossibilities.pop((x,y)) #no longer a possibility, now the definite value

    updateDependentPossibilities(x,y,val)


'''allNeighbors = [((x,y), setOfPossibleVals),....]
'''
def combineOtherSets(allNeighbors, i):
    s = set()
    for j in range(len(allNeighbors)):
        if j != i:
            s.update(allNeighbors[j][1])
    return s


def compareBoxPossibilities():
    #combine all other neighbors (not solved), take difference of cell under inquiry, anything it and only it can be? If so set cell to that value
    for cell in cellFromEachBox:
        allNeighbors = []

        for neighbor in getBoxNeighborCoordList(cell[0], cell[1]):
            if neighbor in cellPossibilities:
                allNeighbors.append((neighbor, cellPossibilities[neighbor]))
                
        for i in range(len(allNeighbors)):
            cellX,cellY = allNeighbors[i][0]
            cellSet = allNeighbors[i][1].copy()
            othersSet = combineOtherSets(allNeighbors,i)
            cellSet.difference_update(othersSet)
            if len(cellSet) == 1: #must be this value
                updateUnknownCell(cellX, cellY, (list(cellSet))[0]) #possible set change as we are iterating over this list of sets issue?
                


def solve():
    
    while True:
        knownState = cellPossibilities.__str__() #state prior to any operations

        for y in range(9):
            row = getRow(y)
            for x in range(9):
                if row[x] != '_':
                    continue #value already known
                
                s = set(["1","2","3","4","5","6","7","8","9"]) #all possibilities
                #start whittling down what cell can be
                neighborSet = set(getBoxNeighbors(x, y))
                s.difference_update(neighborSet)
                
                colSet = set(getCol(x))
                s.difference_update(colSet)
                
                rowSet = set(getRow(y))
                s.difference_update(rowSet)
                                
                if len(s) == 1:#only one value remains, solved the cell
                    updateUnknownCell(x,y, (list(s))[0])
                else:
                    cellPossibilities[(x,y)] = s
            
                
        #completed a single iteration, multiple may be required
        compareBoxPossibilities()
        
        if cellPossibilities.__str__() == knownState: #performed all ops and didn't make any headway... stop looping
            break
        
        
        
def readInGame(q):
    tokens = q.split()
   # numPipes = 0
    currRow = []
    prevCharWasPipe = False
    for t in tokens:
        l = len(currRow)
        if t == '|':
            if l <= 3:
                guardedAppend(3, 100, currRow, prevCharWasPipe)  # 100 is unreachable value in this case
            elif l <= 6:
                guardedAppend(6, 3, currRow, prevCharWasPipe) 
            elif l < 9:
                guardedAppend(9, 6, currRow, prevCharWasPipe) 
            prevCharWasPipe = True
        else:
            # positional value
            currRow.append(t)
            prevCharWasPipe = False
            
        if len(currRow) > 9:
                print("Error")
                exit
        
        if len(currRow) == 9:
            board.append(currRow)
            currRow = []




q = ''' 3 1 _ | _ _ _  | _ _ _  
 _ _ _ | 7 1 _ | _ _ 2
 9 8 2 | _ _ _ | 5 _ 1
 8 _ _ | 1 9 _ | 2 _ 4 
 4 _ _ | _ 5 _ | _ _ 9
 6 _ 5 | _ 8 4 | _ _ 3
 2 _ 6 | _ _ _ | 4 9 5
 7 _ _ | _ 3 5 | _ _ _
 _ _ _ | _ _ _ | _ 3 7'''

readInGame(q)
# print(getRow(0))
#  
# print(getCol(0))
#  
# printBoard()
#  
# print(getBoxNeighbors(8, 8))
# printNeighborsAsBox(8, 8)
solve()
# print (isvalidBoard())
