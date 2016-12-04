'''
Created on Dec 4, 2016

@author: User
'''

if __name__ == '__main__':
    pass

board = []
cellPossibilities = {} #hashMap for position sets (possible values a cell can take)

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
    rowAsArr = []
    row = board[y]
    #Convert to list from raw string
    for i in range(0, 9):
        rowAsArr.append(row[i])

    return rowAsArr

'''Pass in the x you are interested in 
'''
def getCol(x):
    checkPositionRange(x, "From getCol")
    col = []
    for i in range(0,9):
        col.append(getRow(i)[x])
        
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
    
def getNeighbors(x, y):
    checkPositionRange(x, "GetBox x")
    checkPositionRange(y, "GetBox y")
    
    xRange = findNeighborsRanges(x)    
    yRange = findNeighborsRanges(y)
    
    box = []
    for i in range(len(xRange)):
        for j in range(len(yRange)):
            box.append(getPosition(xRange[i], yRange[j]))
    return box

def printNeighborsAsBox(x,y):
    neighbors = getNeighbors(x, y)
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
        
def isvalidBoard():
    for i in range(9):
        if hasDupe(getRow(i)):
            return False
        if hasDupe(getCol(i)):
            return False
        
    cellFromEachBox = [(0,0), (0,4), (0,8), (4,0), (4,4), (4,8), (8,0), (8,4), (8,8)]    

    for cell in cellFromEachBox:
        if hasDupe(getNeighbors(cell[0], cell[1])):
            return False

    return True
        
def guardedAppend(tripletSize, expectedPipePosition, currRow, prevCharWasPipe):
    l = len(currRow)
    
    if l == expectedPipePosition and prevCharWasPipe == False:
        pass  # pipe in expected delimiting position (for a full triplet). No expansion of row representation required
    else: 
        while len(currRow) < tripletSize:
            # Shortcut conditions appear next (meaning skipped a bunch of underscores for notational ease)
            currRow += "_"
    
    return currRow

'''@returns set with 1-9 (inclusive) values
'''
def build1To9Set():
    s = set()
    for i in range(1,10):
        s.add(i)


def updateUnknownCell(x, y, val):
    existingVal = getPosition(x, y)
    if existingVal != '_':
        print("Bad attempt to update cell, tried to overwrite existing " + existingVal + " with " + val)
        exit
    board[y][x] = val


def solve():
    for i in range(9):
        row = getRow(i)
        j = 0
        for r in row:
            if r != '_':
                continue #value already known
            
            s = build1To9Set()
            neighborSet = set(getNeighbors(j, i))
            s.difference_update(neighborSet)
            
            colSet = set(getCol(j))
            s.difference_update(colSet)
            
            rowSet = set(getRow(i))
            s.difference_update(rowSet)
            
            if len(s) == 1:#only one value remains, solved the cell
                updateUnknownCell(j,i, (list(s))[0])
                printBoard()
            else:
                cellPossibilities[(j,i)] = s
            j+=1
        #completed a single iteration, multiple may be required

def readInGame(q):
    tokens = q.split()
   # numPipes = 0
    currRow = ''
    prevCharWasPipe = False
    for t in tokens:
        l = len(currRow)
        if t == '|':
            if l <= 3:
                currRow = guardedAppend(3, 100, currRow, prevCharWasPipe)  # 100 is unreachable value in this case

            elif l <= 6:
                currRow = guardedAppend(6, 3, currRow, prevCharWasPipe) 
            elif l < 9:
                currRow = guardedAppend(9, 6, currRow, prevCharWasPipe) 
            prevCharWasPipe = True
        else:
            # positional value
            currRow += t
            prevCharWasPipe = False
            
        if len(currRow) > 9:
                print("Error")
                exit
        
        if len(currRow) == 9:
            board.append(currRow)
            currRow = ''


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
print(getRow(0))
 
print(getCol(0))
 
printBoard()
 
print(getNeighbors(8, 8))
printNeighborsAsBox(8, 8)
# solve()
print (isvalidBoard())