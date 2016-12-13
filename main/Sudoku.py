'''
Created on Dec 4, 2016

@author: User
'''

from SudokuTools import * 
import cProfile

board = []
cellPossibilities = {}  # hashMap for position sets (possible values a cell can take)

# useful in combo with the findNeighborRange() to get all box members
cellFromEachBox = [(0, 0), (0, 4), (0, 8), (4, 0), (4, 4), (4, 8), (8, 0), (8, 4), (8, 8)]    

totalSolved = 0

#TODO
#exclusionList = cells not to remove possibilities from (ex: in cases where 2 cells in a row have the same 2 values and MUST take those values, eliminating them for other cells, BUT crucially they are still possibilities for these 2 cells (we just don't know which belongs in which yet)
#abstract to be fed a list of cells, then we just feed in neighbors, row, or col
def removeRowPossibilities(rowNum, exclusionList, valueList):
    #iterate over row
    #for each cell in row
    #if not in exclusion list
    #apply all value list removals using the pythonBoilerPlate()
    pass

'''Pass in the y you are interested in 
'''
def getRow(y):
    return board[y]
    
'''Pass in the x you are interested in 
'''
def getCol(x):
    checkPositionRange(x, "From getCol")
    col = []
    for y in range(0, 9):
        col.append(getRow(y)[x])
        
    return col

def getPosition(x, y):
    row = getRow(y)
    return row[x]
    
def getBoxNeighbors(x, y):
    boxMembers = getBoxNeighborCoordList(x, y)
    
    box = []
    for member in boxMembers:
        box.append(getPosition(member[0], member[1]))
    return box


def printNeighborsAsBox(x, y):
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
    totalSolved += 1

    print("{} cells solved:".format(totalSolved))
    
    out = ''
    for y in range(9):  # for reach row
        if y == 3 or y == 6:
            print('----------------------')
        row = getRow(y)
        for x in range(9):  # print a nice spaced, | delimited output
            if x == 3 or x == 6:
                out += '| '
            out += row[x]
            out += ' '
            
        print(out)
        out = ''
        
    print("\n\n")
        
def isvalidBoard():
    for i in range(9):
        if hasDupe(getRow(i)):
            return (False, "Failed verifying row " + str(i))
        if hasDupe(getCol(i)):
            return (False, "Failed verifying column " + str(i))
        
    for cell in cellFromEachBox:
        if hasDupe(getBoxNeighbors(cell[0], cell[1])):
            return (False, "Failed verifying box containing ({},{})".format(cell[0], cell[1]))

    return (True, '')
        
def guardedAppend(tripletSize, expectedPipePosition, currRow, prevCharWasPipe):
    l = len(currRow)
    
    if l == expectedPipePosition and prevCharWasPipe == False:
        pass  # pipe in expected delimiting position (for a full triplet). No expansion of row representation required
    else: 
        while len(currRow) < tripletSize:
            # Shortcut conditions appear next (meaning skipped a bunch of underscores for notational ease)
            currRow.append("_")

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
        pythonBoilerplate((x, t), cellPossibilities, val)
        pythonBoilerplate((t, y), cellPossibilities, val)
        
    for n in getBoxNeighborCoordList(x, y):
        pythonBoilerplate(n, cellPossibilities, val)

def updateUnknownCell(x, y, val):
    existingVal = getPosition(x, y)
    if existingVal != '_':
        print("Bad attempt to update cell ({},{} ), tried to overwrite existing {} with {}".format(x, y, existingVal, val))
        exit
    print("Updating cell ({},{}) to {}".format(x, y, val))
    board[y][x] = val
    
    printBoard()
    
    test = isvalidBoard()
    if test[0] == False:
        print("Broke at this point. " + test[1])
        print(cellPossibilities)
            
    if (x, y) in cellPossibilities:
        cellPossibilities.pop((x, y))  # no longer a possibility, now the definite value

    updateDependentPossibilities(x, y, val)


'''allNeighbors = [((x,y), setOfPossibleVals),....]
'''
def combineOtherSets(allNeighbors, exclusions):
    s = set()
    for xy, possibleVals in allNeighbors:
        if xy not in exclusions:
            s.update(possibleVals)
    return s


def compareBoxPossibilities():
    for cell in cellFromEachBox:
        allNeighbors = []

        for neighbor in getBoxNeighborCoordList(cell[0], cell[1]):
            if neighbor in cellPossibilities:
                allNeighbors.append((neighbor, cellPossibilities[neighbor]))
    
        comparePossibilities(allNeighbors)
        
        findMatchedPossibilities(allNeighbors)    
                
''' Expected list of form [((x,y), {}), ((x1,y1), P{}),...]
They have some commonality (all along a row, column, or within a group (box))
Iterate through, picking a "target cell".
Combine not solved, non-"target" cells, take difference of "target" from group.
Anything it and only it can be? If so set cell to that value, apply new info to possibilities
'''
def comparePossibilities(commonList):
    for xy, possibleVals in commonList:
        othersSet = combineOtherSets(commonList, [xy])
        cellSet = possibleVals.copy()
        cellSet.difference_update(othersSet)
        if len(cellSet) == 1:  # must be the only value left
            updateUnknownCell(xy[0], xy[1], getRemainingVal(cellSet))  # possible set change as we are iterating over this list of sets issue?

    
def compareRowAndColumnPossibilities():
    # rows
    l = []
    for y in range(9):
        for x in range(9):
            if (x, y) in cellPossibilities:
                l.append(((x, y), cellPossibilities[(x, y)]))
                         
        # at each row check
        comparePossibilities(l)
        l = []
    
    # columns
    for x in range(9):
        for y in range(9):
            if (x, y) in cellPossibilities:
                l.append(((x, y), cellPossibilities[(x, y)]))
                         
        # at each column check
        comparePossibilities(l)
        l = []
    
'''If within a group 2 cells have only 2 possible values they can take on, and they are the same values, they elimininate those options for others
TODO generalize to many, this is specific to 2
TODO use for row + column as well, currently only applied to box groups
'''    
def findMatchedPossibilities(commonList):
    for i in range(len(commonList)):
        for j in range(i+1, len(commonList)):
            xyPos, possibleStates = commonList[i]
            xyPos2, possibleStates2 = commonList[j]
            #Do they have the same possible states + only 2 total???
            if possibleStates == possibleStates2 and len(possibleStates) == 2:
                #eliminate the 2 variables as many ways as we can!
                removeThese = list(possibleStates)

                #start with neighbors
                for c in commonList:
                    if c[0] == xyPos or c[0] == xyPos2:
                        pass #they become the 2 states, should not be altered
                    else:
                        pythonBoilerplate(c[0], cellPossibilities, removeThese[0])
                        pythonBoilerplate(c[0], cellPossibilities, removeThese[1])
                        
                        
                #check if they are in line col/row-wise, apply again
                #share a column
                if xyPos[0] == xyPos2[0]:
                    for z in range(8):
                        constructedTuple = (xyPos[0], z)
                        if constructedTuple != xyPos and constructedTuple != xyPos2:
                            pythonBoilerplate(constructedTuple, cellPossibilities, removeThese[0])
                            pythonBoilerplate(constructedTuple, cellPossibilities, removeThese[1])
                
                #share a row
                if xyPos[1] == xyPos2[1]:
                    for z in range(8):
                        constructedTuple = (z, xyPos[1])
                        if constructedTuple != xyPos and constructedTuple != xyPos2:
                            pythonBoilerplate(constructedTuple, cellPossibilities, removeThese[0])
                            pythonBoilerplate(constructedTuple, cellPossibilities, removeThese[1])
                                          
            j+=1


def getRemainingVal(s):
    return list(s)[0]


def solve():
    iterations = 1
    while True:
        knownState = cellPossibilities.__str__()  # state prior to any operations
        print("Iterations of main loop: {}".format(iterations))
        for y in range(9):
            row = getRow(y)
            for x in range(9):
                if row[x] != '_':
                    continue  # value already known
                s = None
                if (x,y) not in cellPossibilities:
                    s = set(["1", "2", "3", "4", "5", "6", "7", "8", "9"])  # all possibilities
                else:
                    s = cellPossibilities[(x,y)]
                # start whittling down what cell can be, only uses definite values, not possible states here
                neighborSet = set(getBoxNeighbors(x, y))
                s.difference_update(neighborSet)
                
                colSet = set(getCol(x))
                s.difference_update(colSet)
                
                rowSet = set(getRow(y))
                s.difference_update(rowSet)
                                
                if len(s) == 1:  # only one value remains, solved the cell
                    updateUnknownCell(x, y, getRemainingVal(s))
                else:
                    cellPossibilities[(x, y)] = s
            
        #Looked for all the simple stuff, move onto non-definite values        
        compareBoxPossibilities()
        compareRowAndColumnPossibilities()

        if cellPossibilities.__str__() == knownState:  # performed all ops and didn't make any headway... stop looping
            print("Not making any progress. Need more solving techniques")
            break
        
        iterations += 1  # TODO Do we really need multiple iterations? Should be enough to just follow the thread that discoveries make...
        
        
def readInGame(q):
    if len(board) > 0: #Read in a new one
        board.clear()
        
    tokens = q.split()
   # numPipes = 0
    currRow = []
    prevCharWasPipe = False
    for t in tokens:
        l = len(currRow)
        if '-------' in t:  # box bottom line (just for visual differentiation purposes)
            continue
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


template = ''' 
 _ _ _  | 5 _ 8  | 1 _ 7  
 _ 3 _  | _ _ _  | _ _ _  
 _ _ 6  | _ _ 9  | _ _ 5  
----------------------
 _ 2 _  | _ _ _  | 8 _ 4  
 _ _ 5  | _ 7 _  | 3 _ _  
 1 _ 3  | _ _ _  | _ 6 _  
 ----------------------
 3 _ _  | 9 _ _  | 6 _ _  
 _ _ _  | _ _ _  | _ 1 _  
 9 _ 4  | 6 _ 5  | _ _ _ 
'''

t2 = '''  
  _ 3 _  | _ _ _  | _ _ 5  
 _ 2 4  | 9 _ _  | _ _ 1  
 _ 6 _  | _ _ 4  | _ _ 7  
----------------------
 _ _ _  | 4 _ 5  | _ 6 _  
 _ _ _  | 3 _ 7  | _ _ _  
 _ 1 _  | 8 _ 2  | _ _ _  
 ----------------------
 8 _ _  | 5 _ _  | _ 2 _  
 4 _ _  | _ _ 3  | 8 7 _  
 3 _ _  | _ _ _  | _ 5 _  '''
# readInGame(t2)

# solve()



def deSerializeGame(uri):
    with open(uri,'r') as f:
        lines = f.readlines()
        return ''.join(lines)
    
# cProfile.run('readInGame(deSerializeGame("../puzzles/inputs/Easy_8313081943")); solve()')

# print(deSerializeGame("../puzzles/inputs/Easy_8313081943"))

#needs work, not using
def serializeSolution():
    
    with open("C:\\Users\\User\\Desktop\\Dev\\workspaces\\LiClipse2\\Sudoku\\output\\easy", "x") as f:
        for row in board:
            for i in len(row):
                f.write(row[i] + " ")
                if i == 2 or i == 5:
                    f.write("\ ")
            f.write("\n")
        

# serializeSolution()